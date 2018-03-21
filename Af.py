#!/usr/bin/env python3
from copy import deepcopy


class Af(object):
    """
        machine exemple constructor
        afd = Af(['1','2'],['a','b'],
       {'1':{'a':['2','3'],'b':['1']},'2':{'a':['1'],'b':['2']}},
       ['1'],['1'])
    """
    (
        STATES,
        ALPHABET,
        TRANSITION_FUNCTION,
        START_STATE,
        FINAL_STATES
    ) = range(5)

    def __init__(self, state, alphabet, relation, start_state, final_state):
        """
        :param state: LISTA  dos estados do automato
        :param alphabet: LISTA com os caracteres aceitos pelo automato
        :param relation: Dicionario da realacao de um estado com o outro
        :param start_state: LISTA estado inicial
        :param final_state: LISTA dos estados finais
        """
        self.machine = (state, alphabet, relation, start_state, final_state)

    def __str__(self):
        """
        Retorna o AF instanciado
        :return: String do af instanciado
        """
        return str(self.machine)

    def __eq__(self, other):
        """
        Verifica a equivalencia de dois automatos
        :param other: Outro objeto (da classe Af)
        :return: True se iguais ou equivalentes
        """
        if not(self.complete_afd() and other.complete_afd()):
            return False

        self.machine[Af.ALPHABET].sort()
        other.machine[Af.ALPHABET].sort()

        if self.machine[Af.ALPHABET] != other.machine[Af.ALPHABET]:
            return False

        not_veri = list()
        startx = self.machine[Af.START_STATE][0]
        starty = other.machine[Af.START_STATE][0]
        if not (startx in self.machine[Af.FINAL_STATES]) == (starty in other.machine[Af.FINAL_STATES]):
            return False

        for e1 in range(len(self.machine[self.STATES])):
            for e2 in range(e1, len(other.machine[other.STATES]), 1):
                if ((self.machine[self.STATES][e1] in self.machine[self.FINAL_STATES]) ==
                        (other.machine[other.STATES][e2] in other.machine[other.FINAL_STATES])):
                    not_veri.append(tuple([self.machine[self.STATES][e1], other.machine[other.STATES][e2]]))

        copy_security = list.copy(not_veri)
        flag = True
        while flag:
            flag = False
            for check in copy_security:
                if check not in not_veri:
                    continue
                if not (check[0] in self.machine[self.FINAL_STATES]) == (check[1] in other.machine[other.FINAL_STATES]):
                    if (check[0] == startx) and (check[1] == starty):
                        return False
                    else:
                        not_veri.remove(check)
                        flag = True
                        continue
                for consume in self.machine[self.ALPHABET]:
                    e1 = self.machine[self.TRANSITION_FUNCTION][check[0]][consume][0]
                    e2 = other.machine[other.TRANSITION_FUNCTION][check[1]][consume][0]
                    if not ((e1 in self.machine[self.FINAL_STATES]) == (e2 in other.machine[
                            other.FINAL_STATES])):
                        if (e1 == startx) and (e2 == starty):
                            return False
                        else:
                            not_veri.remove(check)
                            flag = True
        return True

    def set_new_states(self, state):
        """
        Add estado na maquina
        :param state: no formato de string
        :return: true se possivel adicionar
        """
        try:
            if state not in self.machine[Af.STATES]:
                self.machine[Af.STATES].append(state)
        except SyntaxError:
            return False

        return True

    def set_new_alphabet(self, character):
        """

        :param character: Letra a ser adicionada
        :return: True se sucesso ao tentar adicionar o caracter
        """
        if character in self.machine[Af.ALPHABET]:
            return True
        if (type(character) == str) and (len(character) == 1) and (character not in self.machine[Af.ALPHABET]):
            self.machine[Af.ALPHABET].append(character)
            return True
        else:
            return False

    def set_new_transition(self, source, target, consume):
        """
        adiciona transicao
        :param source: Estado da transicao a ser adicionado
        :param target: Estado para onde ira
        :param consume: Qual caracter sera consumido
        :return: true se possivel adicionar
        """
        if not self.validate_string(consume):
            return False
        try:
            if target in self.machine[Af.TRANSITION_FUNCTION][source][consume]:
                return False
            self.machine[Af.TRANSITION_FUNCTION][source][consume].append(target)
        except KeyError:
            try:
                self.machine[Af.TRANSITION_FUNCTION][source].update({consume: [target]})
            except KeyError:
                self.machine[Af.TRANSITION_FUNCTION].update({source: {consume: [target]}})
        except SyntaxError:
            return False
        return True

    def set_new_start_state(self, state):
        """

        :param state: Estado a ser inicial
        :return: True se possivel
        """
        if (state in self.machine[Af.STATES]) and (state not in self.machine[Af.START_STATE]):
            self.machine[Af.START_STATE].append(state)
            return True
        else:
            return False

    def set_new_final_state(self, state):
        """
        Coloca o estado passado como final
        :param state: Estado a ser final
        :return: True se possivel
        """
        if (state in self.machine[Af.STATES]) and (state not in self.machine[Af.FINAL_STATES]):
            self.machine[Af.FINAL_STATES].append(state)
            return True
        else:
            return False

    def delete_state(self, state):
        """
        Retira o estado e somente ele
        :param state: Estado a ser retirado
        :return: true se possivel retirar
        """
        if state in self.machine[Af.STATES]:
            self.machine[Af.STATES].remove(state)
            if state in self.machine[Af.START_STATE]:
                self.machine[Af.START_STATE].remove(state)
            if state in self.machine[Af.FINAL_STATES]:
                self.machine[Af.FINAL_STATES].remove(state)
            return True
        else:
            return False

    def delete_alphabet(self, character):
        """
        Deleta o caracter
        :param character: caracter a ser retirado
        :return: True se possivel
        """
        try:
            self.machine[Af.ALPHABET].remove(character)
            return True
        except ValueError:
            return False

    def delete_transition(self, source, target, consume):
        """
        Retira a transicao desejada
        :param source: Estado da transicao a ser retirada
        :param target: Estado destino a ser retirado
        :param consume: letra conumida para a remocao
        :return: true se possivel retirar a transicao
        """
        try:
            self.machine[Af.TRANSITION_FUNCTION][source][consume].remove(target)
        except KeyError:
            return False

        if len(self.machine[Af.TRANSITION_FUNCTION][source][consume]) == 0:
            self.machine[Af.TRANSITION_FUNCTION][source].pop(consume)
        return True

    def delete_start_state(self, state):
        """
        Remove o estado como inicial
        :param state: Estado a ser retirado como inicial
        :return: True se possivel
        """
        try:
            self.machine[Af.START_STATE].remove(state)
            return True
        except ValueError:
            return False

    def delete_final_state(self, state):
        """
            Remove o estado como Final
            :param state: Estado a ser retirado como final
            :return: True se possivel
        """
        try:
            self.machine[Af.FINAL_STATES].remove(state)
            return True
        except ValueError:
            return False

    def validate_machine(self):
        """
        verifica se e um af ou seja se esta no seguinte formato
        uma 5-tupla -> as transicoes deve conter todos os caracteres
        ([lista de estados],[lista dos caracteres],{estados e suas relacoes},[lista dos estados iniciais],
        [lista dos estados finais])
        :return: true se e um automato finito aceito
        """
        if type(self.machine[Af.START_STATE]) != list:
            return False
        if type(self.machine[Af.ALPHABET]) != list:
            return False
        if type(self.machine[Af.TRANSITION_FUNCTION]) != dict:
            return False
        if type(self.machine[Af.START_STATE]) != list:
            return False
        if type(self.machine[Af.FINAL_STATES]) != list:
            return False
        return True

    def validate_string(self, word):
        """
        Verifica se a string a ser verificada e permitida
        :param word: String a ser verificada
        :return:Se valido retorna true
        """
        if type(word) != str:
            return False

        for x in word:
            if x not in self.machine[Af.ALPHABET]:
                return False
        return True

    def this_afd(self):
        """
        passa uma maquina AF e Verifica se e um Afd
        :return: True se e um afd e false se nao
        """

        if len(self.machine[Af.START_STATE]) > 1:    # more one start state
            return False

        for x in self.machine[Af.STATES]:
            try:
                transition = list(self.machine[Af.TRANSITION_FUNCTION].get(x).keys())
            except AttributeError:
                continue
            for element in transition:
                if (len(element) > 1) or (element == ''):  # one string is find
                    return False
            for y in self.machine[Af.ALPHABET]:
                try:
                    if len(self.machine[Af.TRANSITION_FUNCTION][x][y]) > 1:      # more one  possibilities
                        return False
                except KeyError:
                    continue
        return True

    def this_afn(self):
        """
        passa uma maquina AF e Verifica se e um Afn
        :return: True se e um afn e false se nao
        """

        for x in self.machine[Af.STATES]:
            try:
                transition = list(self.machine[Af.TRANSITION_FUNCTION].get(x).keys())
            except AttributeError:
                continue
            for element in transition:
                if (len(element) > 1) or (element == ''):  # one string is find
                    return False
        return True

    def this_afv(self):
        """
        passa uma maquina AF e Verifica se e um Afv
        :return: True se e um afv e false se nao
        """

        for x in self.machine[Af.STATES]:
            if x in self.machine[Af.TRANSITION_FUNCTION]:
                transition = list(self.machine[Af.TRANSITION_FUNCTION].get(x).keys())
                for element in transition:
                    if len(element) > 1:  # one string is find
                        return False
        return True

    def this_afe(self):
        """
        passa uma maquina AF e Verifica se e um Afe
        :return: True se e um afe e false se nao
        """
        return self.validate_machine()

    def process_string(self, word):
        """
        Verifica se a maquina Af aceita a string
        :param word: String a ser verificada
        :return: se aceita retorna True
        """
        if not self.this_afd():
            return None     # if self machine not a validate AFD

        if not self.validate_string(word):
            return None

        state = self.machine[Af.START_STATE][0]

        for x in word:
            try:
                state = self.machine[Af.TRANSITION_FUNCTION][state][x][0]
            except KeyError:  # error key
                return False
            except AttributeError:
                return False
        return state in self.machine[Af.FINAL_STATES]

    def mov_test(self, start_state, word):
        """
        Testa movimento da maquina
        :param start_state: estado a se iniciar o teste
        :param word: palavra a ser testada
        :return: estado da parada
        """
        if not self.this_afd():
            return None     # if self machine not a validate AFD

        if not self.validate_string(word):
            return None

        if start_state not in self.machine[Af.STATES]:
            return None

        state = start_state

        for x in word:
            try:
                state = self.machine[Af.TRANSITION_FUNCTION][state][x][0]
            except KeyError:  # error key
                return state

        return state

    def af_is_complete(self):
        """
        Verifica se o af passado e completo
        :return: True se o automato nao ha estado de erro explicito
        """
        for state in self.machine[Af.STATES]:
            for character in self.machine[Af.ALPHABET]:
                try:
                    self.machine[Af.TRANSITION_FUNCTION][state][character]
                except KeyError:  # error key
                    return False
        return True

    def complete_afd(self):
        """
        Completa o afd passado adicionando a ele um estado de erro
        :return:retorna true se o afd foi completado e falso se deu algum  erro
        """
        if self.af_is_complete():
            return True

        self.machine[Af.STATES].append('ERROR')
        self.machine[Af.TRANSITION_FUNCTION]['ERROR'] = {}
        for state in self.machine[Af.STATES]:
            for character in self.machine[Af.ALPHABET]:
                self.machine[Af.TRANSITION_FUNCTION]['ERROR'][character] = ['ERROR']
                try:
                    self.machine[Af.TRANSITION_FUNCTION][state][character]
                except KeyError:  # error key
                    try:
                        self.machine[Af.TRANSITION_FUNCTION][state][character] = ['ERROR']
                    except KeyError:
                        self.set_new_transition(state, 'ERROR', character)
        return True

    def equivalent_states(self):
        """
        :return: Retorna a lista de estados equivalentes
        """
        if not self.this_afd():
            return list()
        if not self.af_is_complete():
            self.complete_afd()

        dont_checked = list()
        flag = True
        for e1 in range(len(self.machine[Af.STATES])):
            for e2 in range(e1, len(self.machine[Af.STATES]), 1):
                dont_checked.append(tuple([self.machine[Af.STATES][e1], self.machine[Af.STATES][e2]]))
        copy_security = dont_checked.copy()
        while flag:
            flag = False
            for check in copy_security:
                if check not in dont_checked:
                    continue
                if (check[0] in self.machine[Af.FINAL_STATES]) != (check[1] in self.machine[Af.FINAL_STATES]):
                    dont_checked.remove(check)
                    flag = True
                    continue
                for character in self.machine[Af.ALPHABET]:
                    e1 = self.machine[Af.TRANSITION_FUNCTION][check[0]][character]
                    e2 = self.machine[Af.TRANSITION_FUNCTION][check[1]][character]
                    e1 = e1[0]
                    e2 = e2[0]
                    if (tuple([e1, e2]) not in dont_checked) and (tuple([e2, e1]) not in dont_checked):
                        dont_checked.remove(check)
                        flag = True
                        break
                    if (e1 in self.machine[Af.FINAL_STATES]) != (e2 in self.machine[Af.FINAL_STATES]):
                        dont_checked.remove(check)
                        flag = True
                        break
        return dont_checked.copy()

    def mini_afd(self):
        """
        Minimiza um AFD
        :param self: AFD a ser minimizado
        :return: true se foi possivel reduzir o automato
        """

        if not self.this_afd():
            return False

        equi = self.equivalent_states()
        for states in equi:
            if states[1] == states[0]:
                continue
            for state in self.machine[Af.STATES]:
                for character in self.machine[Af.ALPHABET]:
                    if self.machine[Af.TRANSITION_FUNCTION][state][character][0] == states[1]:
                        self.machine[Af.TRANSITION_FUNCTION][state][character][0] = states[0]
            try:
                self.delete_state(states[1])
                self.machine[Af.TRANSITION_FUNCTION].pop(states[1])
            except KeyError:
                continue
        sumidouro = self.machine[Af.STATES].copy()
        for state in self.machine[Af.STATES]:
            if state in self.machine[Af.START_STATE]:
                if state in sumidouro:
                    sumidouro.remove(state)
            value = list(self.machine[Af.TRANSITION_FUNCTION].get(state).values())
            for check in value:
                if (check[0] != state) and (check[0] in sumidouro):
                    sumidouro.remove(check[0])
        for s in sumidouro:
            try:
                self.delete_state(s)
                self.machine[Af.TRANSITION_FUNCTION].pop(s)
            except KeyError:
                continue
        return True

    def afn_to_afd(self):
        """
        transforma um afn em um afd
        :return:True se possivel
        """
        if self.this_afd():
            return True
        if not self.af_is_complete():
            self.complete_afd()
        new_start = self.machine[Af.START_STATE]
        new_start.sort()
        not_veri = list()
        not_veri.append(tuple(new_start))
        automato_copy = deepcopy(self.machine)
        self.__init__([], automato_copy[Af.ALPHABET], {}, [], [])
        self.set_new_states(''.join(new_start))
        self.set_new_start_state(''.join(new_start))

        while len(not_veri) != 0:
            nstate = not_veri[0]
            for consume in automato_copy[Af.ALPHABET]:
                new_state = []
                for state in nstate:
                    try:
                        go_to = automato_copy[Af.TRANSITION_FUNCTION][state][consume]
                    except KeyError:
                        continue
                    for i in go_to:
                        if i not in new_state:
                            new_state.append(i)

                new_state.sort()
                not_veri.append(tuple(new_state))
                self.set_new_transition(''.join(nstate), ''.join(new_state), consume)
                if ''.join(new_state) not in self.machine[Af.STATES]:
                    self.set_new_states(''.join(new_state))
                    for s in new_state:
                        if s in automato_copy[Af.FINAL_STATES]:
                            self.set_new_final_state(''.join(new_state))
                            break
                else:
                    not_veri.remove(tuple(new_state))
            not_veri.remove(nstate)
        return True

    def afv_to_afn(self):
        """
        transforma um afv em um afn
        :return: True se possivel
        """
        if self.this_afn():
            return True
        feixo = dict()

        for state in self.machine[Af.STATES]:
            try:
                feixo[state] = self.machine[Af.TRANSITION_FUNCTION][state]['']
            except KeyError:
                continue

        for state in feixo:
            if state in self.machine[Af.START_STATE]:
                try:
                    feixo_mov = feixo[state]
                except KeyError:
                    continue
                for add in feixo_mov:
                    self.set_new_start_state(add)

            for feix in feixo[state]:
                for consume in self.machine[Af.ALPHABET]:
                    try:
                        movimento = self.machine[Af.TRANSITION_FUNCTION][feix][consume]
                    except KeyError:
                        continue

                    for stat in movimento:
                        try:
                            feixo_mov = feixo[stat]
                        except KeyError:
                            feixo_mov = [stat]
                        for adiciona in feixo_mov:
                            self.set_new_transition(state, adiciona, consume)

                    self.delete_transition(state, feix, '')

        return True

    def afe_to_afv(self):
        """
        Transforma um afe em um afv
        :return: True se foi possivel transformar
        """
        if self.this_afv():
            return True
        auxiliar = deepcopy(self.machine)
        for state in auxiliar[Af.STATES]:
            if state in auxiliar[Af.TRANSITION_FUNCTION]:
                for key in auxiliar[Af.TRANSITION_FUNCTION][state].keys():
                    if len(key) > 1:
                        targets = self.machine[Af.TRANSITION_FUNCTION][state][key]
                        cont = 0
                        for target in targets:
                            self.set_new_transition(state, state+str(cont), key[0])
                            for new in key[1:-1]:
                                self.set_new_states(state+str(cont))
                                self.set_new_transition(state+str(cont), state+str(cont+1), new)
                                cont = cont + 1
                            self.set_new_states(state + str(cont))
                            self.set_new_transition(state + str(cont), target, key[-1])
                            self.delete_transition(state, target, key)
                            cont = cont + 1
        return True

    def multi_auto(self, other):
        """
        Faz a multiplicacao do automato AFD
        :param other: objeto da classe Af
        :return: automato multiplicado se possivel e um novo objeto da classe Af
        """
        temp = Af([], [], {}, [], [])

        state = ''.join(self.machine[Af.START_STATE] + other.machine[other.START_STATE])
        temp.set_new_states(state)
        temp.set_new_start_state(state)

        for alph in self.machine[Af.ALPHABET]:
            temp.set_new_alphabet(alph)
        for alph in other.machine[Af.ALPHABET]:
            temp.set_new_alphabet(alph)

        estate1 = self.machine[Af.START_STATE][0]
        estate2 = other.machine[Af.START_STATE][0]

        not_cheked = list()
        not_cheked.append(tuple([estate1, estate2]))
        cheked = list()
        flag = True
        e1 = None
        e2 = None
        while flag:

            for consume in temp.machine[Af.ALPHABET]:
                before = ''.join(estate1+estate2)
                try:
                    e1 = self.machine[Af.TRANSITION_FUNCTION][estate1][consume][0]
                    e2 = other.machine[Af.TRANSITION_FUNCTION][estate2][consume][0]
                except KeyError:
                    pass
                after = ''.join(e1+e2)
                temp.set_new_states(after)
                temp.set_new_transition(before, after, consume)
                if (tuple([e1, e2]) not in not_cheked) and (tuple([e1, e2]) not in cheked) :
                    not_cheked.append(tuple([e1, e2]))

            cheked.append(tuple([estate1, estate2]))
            not_cheked.remove(tuple([estate1, estate2]))
            if len(not_cheked) != 0:
                estate1 = not_cheked[0][0]
                estate2 = not_cheked[0][1]
            else:
                flag = False
        return deepcopy(temp)

    def union_automato(self, other):
        """
        Retorna a uniao de dois automatos
        :param other: Objeto da classe dos automatos
        :return: Automato uniao
        """
        temp = self.multi_auto(other)
        i=0
        flag = True
        finalx = None
        finaly = None
        while flag:
            flag = False
            if i < len(other.machine[Af.FINAL_STATES]):
                flag = True
                finaly = other.machine[Af.FINAL_STATES][i]
            if i < len(self.machine[Af.FINAL_STATES]):
                Flag = True
                finalx =  self.machine[Af.FINAL_STATES][i]
            for state in temp.machine[Af.STATES]:
                if finalx in state:
                    temp.set_new_final_state(state)
                elif finaly in state:
                    temp.set_new_final_state(state)
            i = i + 1
        return deepcopy(temp)

    def intercect_automato(self, other):
        """

        :param other:
        :return:
        """
        if not self.af_is_complete():
            self.complete_afd()
        if not other.af_is_complete():
            other.complete_afd()
        temp = self.multi_auto(other)
        for finalx in self.machine[Af.FINAL_STATES]:
            for finaly in other.machine[Af.FINAL_STATES]:
                temp.set_new_final_state(''.join(finalx + finaly))

        return deepcopy(temp)

    def difere_automato(self, other):
        """
        Retorna a diferenca entre dois automatos
        :param other: objeto da classe Af
        :return: Automato
        """
        aux_other = deepcopy(other)
        aux_other.neg_automato()
        return self.intercect_automato(aux_other)

    def neg_automato(self):
        """
        Negacao de um automato
        :return: true se automato negado
        """
        if not self.af_is_complete():
            self.complete_afd()

        for state in self.machine[Af.STATES]:
            if state in self.machine[Af.FINAL_STATES]:
                self.delete_final_state(state)
            else:
                self.set_new_final_state(state)
        return True
