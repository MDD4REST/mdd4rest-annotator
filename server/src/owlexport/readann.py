from sys import stderr
from .transformationmap import transformit


def is_int(val):
    try:
        num = int(val)
    except ValueError:
        return False
    return True


class Entity:
    def __init__(self, entity_id, entity_type, entity_text):
        self.entity_id = entity_id
        self.entity_type = entity_type
        self.entity_text = '_'.join(entity_text.split())

    def __str__(self):
        return str(self.entity_id) + "." + self.entity_text + ":" + self.entity_type

    def owl(self):
        return self.entity_type, self.entity_text + "_" + str(self.entity_id), self.entity_text

    def nameid(self):
        return self.entity_text + "_" + str(self.entity_id)


class Attribute:
    def __init__(self, attribute_id, attribute_type, attribute_text, entity_id, is_entity):
        self.attribute_id = attribute_id
        self.attribute_type = attribute_type
        self.attribute_text = '_'.join(attribute_text.split())
        self.entity_id = entity_id
        self.is_entity = is_entity

    def __str__(self):
        return str(self.attribute_id) + "." + self.attribute_text + ":" + self.attribute_type + "-" + str(self.entity_id)

    def owl(self):
        return self.attribute_type, self.attribute_text, self.entity_id, self.is_entity

    def nameid(self):
        return self.attribute_text + "_" + str(self.attribute_id)


class Association:
    def __init__(self, association_id, association_type, entity_a, entity_b):
        self.association_id = association_id
        self.association_type = association_type
        self.entity_a = entity_a
        self.entity_b = entity_b

    def __str__(self):
        return str(self.association_id) + "." + self.association_type + ":" + str(self.entity_a) + "-" + str(self.entity_b)

    def owl(self):
        return self.entity_a, self.association_type, self.entity_b


class Event:
    def __init__(self, event_id, event_entity, entity_a, entity_b, entity_a_type, entity_b_type):
        self.event_id = event_id
        self.event_entity = event_entity
        self.entity_a = entity_a
        self.entity_b = entity_b
        self.entity_a_type = entity_a_type
        self.entity_b_type = entity_b_type

    def __str__(self):
        return str(self.event_id) + "." + str(self.event_entity) + ":" + self.entity_a_type + "." + str(self.entity_a) + "-" + self.entity_b_type + "." + str(self.entity_b)

    def owl(self):
        return self.event_entity, self.entity_a_type, self.entity_a, self.entity_b_type, self.entity_b


class Requirement:
    def __init__(self, requirement_text, requirement_id):
        self.reqid = requirement_id
        self.reqtext = requirement_text.replace(':', '_').replace(
            '/', '_').replace('\'', '_').replace('\xe2\x80\x99', '_')
        self.entities = []
        self.associations = []
        self.events = []
        self.attributes = []

    def add_entity(self, entity_data):
        self.entities.append(
            Entity(int(entity_data[0][1:]), entity_data[1].split()[0], entity_data[-1]))

    def has_entity(self, entity_id):
        return entity_id in [s.entity_id for s in self.entities]

    def has_event(self, event_id):
        return event_id in [s.event_id for s in self.events]

    def add_association(self, association_data):
        assoc = association_data[-1].split()
        self.associations.append(Association(int(association_data[0][-1]), assoc[0], int(
            assoc[1].split(':T')[-1]), int(assoc[2].split(':T')[-1])))

    def add_event(self, event_data):
        assoc = event_data[-1].split()
        self.events.append(Event(
            int(event_data[0][-1]),
            int(assoc[0].split(':T')[-1]),
            int(assoc[1].split(':T')[-1]),
            int(assoc[2].split(':T')[-1]),
            assoc[1].split(':T')[0],
            assoc[2].split(':T')[0]
        ))

    def add_attribute(self, attr_data, entity):
        assoc = attr_data[-1].split()
        if entity:
            self.attributes.append(Attribute(
                int(attr_data[0][-1]),
                assoc[0],
                assoc[2],
                int(assoc[1].split('T')[-1]),
                True
            ))
        else:
            self.attributes.append(Attribute(
                int(attr_data[0][-1]),
                assoc[0],
                assoc[2],
                int(assoc[1].split('E')[-1]),
                False
            ))

    def __str__(self):
        txtt = "Requirement " + str(self.reqid) + "\n"
        txtt = "Text: " + self.reqtext + "\n"
        txtt += "Entities: (" + '), ('.join(map(str, self.entities)) + ")\n"
        txtt += "Associations: (" + '), ('.join(map(str,
                                                    self.associations)) + ")\n"
        return txtt

    def get_entity_by_id(self, entity_id):
        print("ent", entity_id, file=stderr)
        # print("entities",  [s.entity_id for s in self.entities], file=stderr)
        for s in self.entities:
            if s.entity_id == entity_id:
                print("s", s, file=stderr)
        return [s for s in self.entities if s.entity_id == entity_id][0]

    def get_event_by_id(self, event_id):
        return [s for s in self.events if s.event_id == event_id][0]

    def get_entities(self):
        for entity in self.entities:
            yield entity.owl()

    def get_associations(self):
        for association in self.associations:
            a, r, b = association.owl()
            a = self.get_entity_by_id(a)
            b = self.get_entity_by_id(b)
            yield a.owl(), r, b.owl()

    def get_events(self):
        for events in self.events:
            event_entity, a_type, a, b_type, b = events.owl()
            a = self.get_entity_by_id(a)
            b = self.get_entity_by_id(b)
            event_entity = self.get_entity_by_id(event_entity)
            yield event_entity.owl(), a_type, a.owl(), b_type, b.owl()

    def get_attributes(self):
        for attribute in self.attributes:
            type, text, entity_id, is_entity = attribute.owl()
            if (is_entity):
                ent = self.get_entity_by_id(entity_id)
            else:
                ent = self.get_event_by_id(entity_id)
            yield type, text, ent.owl(), is_entity

    def treqid(self):
        return 'FR' + str(self.reqid)


class Project:
    def __init__(self, name, filename, req_to_read=None):
        self.req_to_read = req_to_read
        self.name = name
        self.reqs = []
        self.read_ann(filename)

    def get_event_text(self, event, req):
        event_entity, a_type, a, b_type, b = event
        a = req.get_entity_by_id(a).owl()
        b = req.get_entity_by_id(b).owl()
        event_entity = req.get_entity_by_id(event_entity).owl()
        event_name = self.entitycorr[event_entity[0] + event_entity[2]] + '__' + \
            event_entity[0] + '__' + \
            transformit[a_type] + '__' + \
            self.entitycorr[a[0] + a[2]] + '__' + \
            transformit[b_type] + '__' + \
            self.entitycorr[b[0] + b[2]]
        return event_name

    def read_ann(self, filename):
        with open(filename + '.txt') as txtfile:
            passage = txtfile.read()
            sentences = [s.strip() for s in passage.split('\n') if s.strip()]
            for i, sentence in enumerate(sentences):
                self.reqs.append(Requirement(sentence, i + 1))

        def get_reqid_by_index(indexb):
            return passage[0:indexb].count('\n')

        def get_reqid_by_entity_index(indexb):
            for i, req in enumerate(self.reqs):
                if req.has_entity(indexb):
                    return i
            return None

        def get_reqid_by_event_index(indexb):
            for i, req in enumerate(self.reqs):
                if req.has_event(indexb):
                    return i
            return None

        with open(filename + '.ann') as annfile:
            annotations = [s.strip() for s in annfile.readlines()]

        for annotation in annotations:
            if annotation[0] == 'T':
                # entity
                annotation = annotation.split('\t')
                print("ann", annotation,annotation[1].split()[-1], file=stderr)
                reqid = get_reqid_by_index(int(annotation[1].split()[-1]))
                print("req", reqid, file=stderr)
                if (not self.req_to_read) or reqid == self.req_to_read - 1:
                    self.reqs[reqid].add_entity(annotation)
            elif annotation[0] == 'R':
                # association
                annotation = annotation.split('\t')
                reqid = get_reqid_by_entity_index(
                    int(annotation[-1].split()[-1].split(':T')[-1]))
                if (not self.req_to_read) or reqid == self.req_to_read - 1:
                    self.reqs[reqid].add_association(
                        annotation)
            elif annotation[0] == 'E':
                # events
                annotation = annotation.split('\t')
                reqid = get_reqid_by_entity_index(
                    int(annotation[-1].split()[-1].split(':T')[-1]))
                if (not self.req_to_read) or reqid == self.req_to_read - 1:
                    self.reqs[reqid].add_event(annotation)

            elif annotation[0] == 'A':
                annotation = annotation.split('\t')
                entity_id = annotation[-1].split()[1].split('T')[-1]
                event_id = annotation[-1].split()[1].split('E')[-1]
                entity = True
                reqid = 0
                if is_int(entity_id):
                    reqid = get_reqid_by_entity_index(int(entity_id))
                elif is_int(event_id):
                    entity = False
                    reqid = get_reqid_by_event_index(int(event_id))

                if (not self.req_to_read) or reqid == self.req_to_read - 1:
                    self.reqs[reqid].add_attribute(annotation, entity)
                # entityreqid = get_reqid_by_entity_index(
                #     )

    def requirements(self):
        return ((req.treqid(), req.reqtext) for req in self.reqs)

    def entities(self):
        self.namecorr = {}
        self.entitycorr = {}
        for req in self.reqs:
            events_list = list(
                map(lambda x: x[0][0] + x[0][2], req.get_events()))
            for entity in req.get_entities():
                check_text = entity[0] + entity[2]
                if check_text not in events_list:
                    if check_text not in self.entitycorr:
                        if entity[2] not in self.namecorr:
                            self.namecorr[entity[2]] = 0
                        else:
                            self.namecorr[entity[2]] += 1
                        self.entitycorr[check_text] = (entity[2] + '_' + str(
                            self.namecorr[entity[2]])) if self.namecorr[entity[2]] > 0 else entity[2]
                        yield req.treqid(), (entity[0], self.entitycorr[check_text], entity[2]), True
                    else:
                        yield req.treqid(), (entity[0], self.entitycorr[check_text], entity[2]), False
                else:
                    self.entitycorr[check_text] = entity[2]

    def associations(self):
        for _ in self.entities():
            pass
        assocset = set()
        for req in self.reqs:
            print("req", req.reqid, req.treqid(), req.reqtext, [
                  s.entity_id for s in req.entities], file=stderr)
            for association in req.get_associations():
                entity0 = association[0]
                entity1 = association[2]
                if self.entitycorr[entity0[0] + entity0[2]] + association[1] + self.entitycorr[entity1[0] + entity1[2]] not in assocset:
                    assocset.add(self.entitycorr[entity0[0] + entity0[2]] +
                                 association[1] + self.entitycorr[entity1[0] + entity1[2]])
                    yield self.entitycorr[entity0[0] + entity0[2]], association[1], self.entitycorr[entity1[0] + entity1[2]]

    def events(self):
        for _ in self.entities():
            pass
        assocset = set()
        for req in self.reqs:
            for event in req.get_events():
                entity0 = event[0]
                entity1 = event[2]
                entity2 = event[4]
                event_name = self.entitycorr[entity0[0] + entity0[2]] + '__' + \
                    entity0[0] + '__' + \
                    transformit[event[1]] + '__' + \
                    self.entitycorr[entity1[0] + entity1[2]] + '__' + \
                    transformit[event[3]] + '__' + \
                    self.entitycorr[entity2[0] + entity2[2]]

                if event_name not in assocset:
                    assocset.add(event_name)
                    yield event_name, \
                        entity0[0], \
                        self.entitycorr[entity1[0] + entity1[2]], \
                        event[1], \
                        self.entitycorr[entity2[0] + entity2[2]], \
                        event[3], \
                        self.entitycorr[entity0[0] + entity0[2]]

    def attributes(self):
        assocset = set()
        for req in self.reqs:
            for type, text, ent, is_entity in req.get_attributes():
                if(is_entity):
                    ent_name = self.entitycorr[ent[0] + ent[2]]
                else:
                    ent_name = self.get_event_text(ent, req)
                yield type, text, ent_name, is_entity
