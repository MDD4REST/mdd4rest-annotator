import re
from ontosPy.ontosPy import Ontology
from rdflib import Graph, URIRef, Literal

class ExtOntology(Ontology):
	def __init__(self, uri=False):
		super(ExtOntology, self).__init__(uri)
		self.ONTOLOGY_ADDRESS = self.ontologyNamespaces()[0][1]
		self.TYPE = [j for i, j in self.ontologyNamespaces() if i == "rdf"][0] + "type"
		self.COMMENT = [j for i, j in self.ontologyNamespaces() if i == "rdfs"][0] + "comment"
		self.uri = uri
	def add_individual(self, class_name, individual_name, comment_name = ""):
		self.rdfGraph.add((URIRef(self.ONTOLOGY_ADDRESS + individual_name), self.TYPE, URIRef(self.ONTOLOGY_ADDRESS + class_name)))
		self.rdfGraph.add((URIRef(self.ONTOLOGY_ADDRESS + individual_name), self.COMMENT, Literal(comment_name)))
	def add_property(self, individual_name1, property_name, individual_name2):
		self.rdfGraph.add((URIRef(self.ONTOLOGY_ADDRESS + individual_name1), self.ONTOLOGY_ADDRESS + property_name, URIRef(self.ONTOLOGY_ADDRESS + individual_name2)))
	def add_datatype(self, individual_name1, property_name, datatype):
		self.rdfGraph.add((URIRef(self.ONTOLOGY_ADDRESS + individual_name1), self.ONTOLOGY_ADDRESS + property_name,  Literal(datatype)))
	def is_operation(self, theclass):
		return str([i.split('#')[1] for i in self.classAllSupers(self.classFind('http://www.owl-ontologies.com/Ontology1273059028.owl#' + theclass, exact = True)[0])][1]) == "OperationType"
	def read_in_blocks(self, obj):
		cblock = ""
		for line in obj.decode().split('\n'):
			if not line.strip():
				if cblock:
					yield cblock
				cblock = ""
			else:
				cblock += line + '\n'
	def get_ttl(self):
		def change_comment_to_label(name, comment):
			name = name[1:].split()[0]
			pattern = r'"([^"]*)"'
			return re.sub(pattern, "\"" + name + "\"", comment.replace("rdfs:comment", "rdfs:label").replace('.', ';').replace(';\"', '.\"'))
		blocks = ["""@prefix :      <http://www.owl-ontologies.com/Ontology1273059028.owl#> .\n@prefix rdfs:  <http://www.w3.org/2000/01/rdf-schema#> .\n@prefix rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n"""]
		for block in self.read_in_blocks(self.rdfGraph.serialize(format = 'n3')):
			if block[0] != '@' and block[0] != '<' and block[0] != '[' and 'owl:' not in block.split('\n')[0]:
				block = block.split('\n')[:-1]
				newblock = [block[0]]
				newblock.append(block[-1].replace("rdfs:comment", "rdf:comment").replace('.', ';').replace(';\"', '.\"'))
				newblock.append(change_comment_to_label(block[0], block[-1]))
				for b in block[1:-1]:
					newblock.append(b)
				newblock[-1] = newblock[-1].replace(';', '.')
				blocks.append('\n'.join(newblock) + '\n')
		return (block for block in blocks)
	def close(self):
		# with open(self.uri, 'w', encoding="utf-8") as outfile:
			# outfile.write(self.rdfGraph.serialize())
		self.rdfGraph.serialize(destination= self.uri)
		# with open(self.uri[:-4] + '.ttl', 'wb') as outfile:
		# 	outfile.write('\n'.join(self.get_ttl()).encode())

