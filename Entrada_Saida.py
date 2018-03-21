#!/usr/bin/env python3
import xml.etree.cElementTree as ET
from xml.etree.cElementTree import ElementTree
from xml.dom import minidom
from Af import Af


class Entrada_Saida(object):

    def __init__(self):
        self.estados = []
        self.alphabet = []
        self.transitions = {}
        self.estados_iniciais = []
        self.estados_finais = []

    def load(self, diretorio):
        """
            Le todo o arquivo para uma variavel do tipo ElementTree
            percorre a variavel ElementTree pegando as informacoes
            necessarias para montar o automato
        """
        # pegando o diretorio base
        # base_path = os.path.dirname(os.path.realpath(__file__))
        # base_path = base_path + '\\' + diretorio
        # diretorio = base_path

        # lendo o arquivo xml tree usando elementtree
        self.__init__()

        tree = ElementTree()  # instanciando o ElementTree
        tree.parse(diretorio)  # lendo o conteudo diretorio para dentro de tree
        tree._setroot(tree.find("structure/structure"))  # setando o root mais adequado
        root = tree.getroot()  # pegando o root setado

        #  tipo variavel que vai guarda o conteudo da tag type
        for child in root:
            tipo = child.attrib['type']  # pegando o conteudo da tag type

            if tipo == "start_state":  # get the start states
                for child2 in child:
                    for child3 in child2:
                        if child3.tag == "name":
                            self.estados_iniciais.append(child3.text)  # adicionando elemento a lista de estados iniciais
                            break

            if tipo == "input_alph":  # get the alphabet from automat
                for child2 in child:
                    self.alphabet.append(child2.text)  # adicionando elemento a lista com as letras do alfabeto

            if tipo == "final_states":  # get the final states
                for child2 in child:
                    for child3 in child2:
                        if child3.tag == "name":
                            self.estados_finais.append(child3.text)  # adicionando elemento a lista de estados finais
                            break

            if tipo == "transition_set":  # pega as conexoes entre os estados
                inp = ""        # armazena o input
                para = ""       # armazena o estado de entrada
                de = ""         # armazena o estado de saida

                flag = ""       # variavel que ajuda a
                entradas = []   # verificar se um novo dicionario deve ser criado dentro do dicionario principal

                for child2 in child:
                    for child3 in child2:
                        if child3.tag == "from":  # get estado de saida
                            for child4 in child3:
                                if (child4.tag == "name"):
                                    de = child4.text
                                    break

                        if child3.tag == "input":  # get input
                            inp = child3.text

                        if child3.tag == "to":
                            for child4 in child3:
                                if child4.tag == "name":  # get estado de entrada
                                    para = child4.text
                                    break

                    if flag != de:  # verifica se o estado de entrada ja foi alocado dentro da estrutura principal
                        flag = de  # atribui o novo estado a flag
                        self.transitions[de] = {}  # aloca um dicionario para dentro do dicionario principal na chave "de"
                        del entradas[:]  # limpa a lista de

                    try:
                        self.transitions[de][inp].append(para)
                    except KeyError:
                        self.transitions[de][inp] = []  # aloca uma lista para cada letra do alfabeto
                        self.transitions[de][inp].append(para)  # adiciona um elemento ao dicionario

            if tipo == "state_set":  # pega todos os estados usados no automato
                for child2 in child:
                    for child3 in child2:
                        if child3.tag == "name":
                            self.estados.append(child3.text)  # adiciona elemento a lista "estados"
                            break
        return Af(self.estados, self.alphabet, self.transitions, self.estados_iniciais, self.estados_finais)

    def load_jff(self, diretorio):
        """

        :param diretorio:
        :return:
        """
        tree = ET.parse(diretorio)
        root = tree.getroot()
        temp = Af([], [], {}, [], [])
        automaton = root.find('automaton')
        for states in automaton.findall('state'):
            state = states.get('name')
            temp.set_new_states(state)
            final = states.find('final')
            inicial = states.find('initial')
            if not(final is None):
                temp.set_new_final_state(state)
            if not(inicial is None):
                temp.set_new_start_state(state)
        sourcename = None
        targetname = None
        for transicao in automaton.findall('transition'):
            source = transicao.find('from').text
            target = transicao.find('to').text
            consume = transicao.find('read').text
            for i, state in enumerate(temp.machine[Af.STATES]):
                if source == str(i):
                    sourcename = state
                if target == str(i):
                    targetname = state
            if consume is None:
                consume = ''
            for alph in consume:
                temp.set_new_alphabet(alph)
            temp.set_new_transition(sourcename, targetname, consume)

        return temp

    def salve_jff(self, automato, diretorio):
        """

        :param automato:
        :param diretorio:
        :return:
        """
        estrutura = ET.Element('structure')
        tipo = ET.SubElement(estrutura, 'type')
        tipo.text = 'fa'
        automaton = ET.SubElement(estrutura, 'automaton')
        for i, states in enumerate(automato.machine[Af.STATES]):
            state = ET.SubElement(automaton, 'state')
            state.set('id', str(i))
            state.set('name', states)
            if states in automato.machine[Af.FINAL_STATES]:
                ET.SubElement(state, 'final')
            if states in automato.machine[Af.START_STATE]:
                ET.SubElement(state, 'initial')
        idsource = None
        idtarget = None
        for source in automato.machine[Af.TRANSITION_FUNCTION].keys():
            for consume in automato.machine[Af.TRANSITION_FUNCTION][source].keys():
                for target in automato.machine[Af.TRANSITION_FUNCTION][source][consume]:
                    transition = ET.SubElement(automaton, 'transition')

                    froms = ET.SubElement(transition, 'from')
                    to = ET.SubElement(transition, 'to')
                    read = ET.SubElement(transition, 'read')

                    for i, state in enumerate(automato.machine[Af.STATES]):
                        if state == source:
                            idsource = str(i)
                        if state == target:
                            idtarget = str(i)

                    froms.text = idsource
                    to.text = idtarget
                    read.text = consume

        file = open(diretorio, 'w+')
        file.write(Entrada_Saida.prettify(estrutura))
        file.close()
        return True

    #esse metodo nao e de minha autoria peguei na internet para embelezar o xml de saida
    @staticmethod
    def prettify(elem):
        """Return a pretty-printed XML string for the Element.
        """
        rough_string = ET.tostring(elem, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")
