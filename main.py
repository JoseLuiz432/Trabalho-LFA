#!/usr/bin/env python3

from entrada_saida import Entrada_Saida
from af import Af


class Main(object):

    @staticmethod
    def main():

        automatos = list()
        indice_maquina = 0
        print("""
                    ######################################################
                    #                Automatos Finitos                   #
                    #version jflap:                                      #
                    #Leitura: JFLAP8(beta) e JFLAP7                      #
                    #Escrita: JFLAP7                                     #
                    ######################################################
              """)
        flag = True
        inout = Entrada_Saida()
        while flag:
            try:
                escolha = int(input('Deseja 0-criar ou 1-importar o automato: '))
            except ValueError:
                print('Valor invalido')
                continue
            if escolha == 0:
                auto = Af([], [], {}, [], [])
                automatos.append(auto)
                entrada = input('Informe os estados presentes: ') + ' '
                estados = list()
                nome_estado = str()
                for ex in entrada:
                    if ex == ' ':
                        estados.append(nome_estado)
                        nome_estado = ''
                    else:
                       nome_estado = nome_estado + ex
                for state in estados:
                    auto.set_new_states(state)

                entrada = input('Informe o Alfabeto: ') + ' '
                alfabeto = list()
                letra = str()
                for ex in entrada:
                    if ex == ' ':
                        alfabeto.append(letra)
                        letra = ''
                    else:
                        letra = letra + ex
                for alph in alfabeto:
                    print(alph)
                    auto.set_new_alphabet(alph)

                    print('Transicoes: ')
                while True:

                    print('##################################################################')
                    print('#Construcao %s #' %auto)
                    print('##################################################################')
                    print('-----------------criar de transição------------')
                    source = input('Informe o estado source: ')
                    target = input('Informe o estado target: ')
                    consume = input('informe o consume: ')
                    auto.set_new_transition(source, target, consume)
                    escolha = input('0- para uma nova transicao, 1-para encerrar')
                    if escolha == '1':
                        break
                entrada = input('Informe os estados iniciais: ') + ' '
                estados = list()
                nome_estado = str()
                for ex in entrada:
                    if ex == ' ':
                        estados.append(nome_estado)
                        nome_estado = ''
                    else:
                        nome_estado = nome_estado + ex
                for state in estados:
                    auto.set_new_start_state(state)

                entrada = input('Informe os estados finais: ') + ' '
                estados = list()
                nome_estado = str()
                for ex in entrada:
                    if ex == ' ':
                        estados.append(nome_estado)
                        nome_estado = ''
                    else:
                        nome_estado = nome_estado + ex
                for state in estados:
                    auto.set_new_final_state(state)

            else:
                diretorio = input('Informe o diretorio do automato com a extensao .jflap ou .jff: ')
                try:
                    if '.jff' in diretorio:
                        automatos.append(inout.load_jff(diretorio))
                    else:
                        automatos.append(inout.load(diretorio))
                except FileNotFoundError:
                    print('Arquivo nao encontrado')
                    continue

            while flag:
                print('######################################################')
                print('#          Menu de Operacoes Automatos Finitos       #')
                print('#1 - Tipo do automato (Afd, Afn, Afv ou Afe          #')
                print('#2 - Verifica se o automato e completo               #')
                print('#3 - Completa o Automato                             #')
                print('#4 - Informa os Estados equivalentes do Automato(AFD)#')
                print('#5 - Minimiza o automato (AFD)                       #')
                print('#6 - Testar Movimentacao (AFD)                       #')
                print('#7 - Testar String       (AFD)                       #')
                print('#8 - Transformar AFE->AFV                            #')
                print('#9 - Transformar AFV->AFN                            #')
                print('#10- Transformar AFN->AFD                            #')
                print('#11- Operacoes entre dois automatos                  #')
                print('#12- Salvar automato como .jff                       #')
                print('#13- Criar outro automato                            #')
                print('#14- Adicionar estado                                #')
                print('#15- Adicionar Alfabeto                              #')
                print('#16- Adicionar Transicao                             #')
                print('#17- Adicionar Estado Inicial                        #')
                print('#18- Adicionar Estado Final                          #')
                print('#19- Deletar estado                                  #')
                print('#20- Deletar Alfabeto                                #')
                print('#21- Deletar Transicao                               #')
                print('#22- Deletar Estado Inicial                          #')
                print('#23- Deletar Estado Final                            #')
                print('#0 - Exit                                            #')
                print('######################################################')
                print('')

                try:
                    choice = int(input())
                except ValueError:
                    print('Valor incorreto')
                    continue

                if choice == 0:
                    flag = False
                    continue
                elif choice == 13:
                    indice_maquina = indice_maquina + 1
                    break

                cont = 0
                print('#######################################################')
                print('#                Maquinas resgistradas                #')
                for m in automatos:
                    print('%i - %s' % (cont, m))
                    cont = cont + 1
                print('#######################################################')
                try:
                    maquina = int(input('Informe a maquina: '))
                except ValueError:
                    print('Valor incorreto')
                    continue

                if maquina > indice_maquina:
                    print('Maquina nao encontrada')
                    continue

                if choice == 1:
                    if automatos[maquina].this_afd():
                        print('Automato e um AFD')
                    elif automatos[maquina].this_afn():
                        print('Automato e um AFN')
                    elif automatos[maquina].this_afv():
                        print('Automato e um AFV')
                    elif automatos[maquina].this_afe():
                        print('Automato e um AFE')
                elif choice == 2:
                    if automatos[maquina].af_is_complete():
                        print('E completo')
                    else:
                        print('Nao e completo')
                elif choice == 3:
                    if automatos[maquina].complete_afd():
                        print('Sucesso')
                    else:
                        print('Erro ao tentar completar o automato')
                elif choice == 4:
                    print(automatos[maquina].equivalent_states())
                elif choice == 5:
                    if automatos[maquina].mini_afd():
                        print('Sucesso')
                    else:
                        print('Erro ao tentar minimizar')
                elif choice == 6:
                    word = input('Informe a palavra a ser verificada: ')
                    state = input('Informe o estado inicial: ')
                    print('Estado da parada: ')
                    print(automatos[maquina].mov_test(state, word))
                elif choice == 7:
                    word = input('Informe a palavra a ser verificada: ')
                    if automatos[maquina].process_string(word):
                        print('Palavra foi aceita')
                    else:
                        print('Palavra nao foi aceita')
                elif choice == 8:
                    if automatos[maquina].afe_to_afv():
                        print('Sucesso')
                    else:
                        print('ERRO')
                elif choice == 9:
                    if automatos[maquina].afv_to_afn():
                        print('Sucesso')
                    else:
                        print('ERRO')
                elif choice == 10:
                    if automatos[maquina].afn_to_afd():
                        print('Sucesso')
                    else:
                        print('ERRO')

                elif choice == 11:
                    print('Infome a segunda maquina: ')
                    cont = 0
                    print('#######################################################')
                    print('#                Maquinas resgistradas                #')
                    for m in automatos:
                        print('%i - %s' % (cont, m))
                        cont = cont + 1
                    print('#######################################################')
                    maquina2 = int()
                    try:
                        maquina2 = int(input('Informe a maquina: '))
                    except ValueError:
                        print('Valor incorreto')
                        continue
                    print('#######################################################')
                    print('#Infome a operacao                                    #')
                    print('#0 - Verificar se as maquinas  sao equivalentes       #')
                    print('#1 - Multiplicacao de automatos                       #')
                    print('#2 - Uniao de automatos                               #')
                    print('#3 - Intercecao de automatos                          #')
                    print('#4 - Diferenca de automatos                           #')
                    print('#######################################################')
                    try:
                        choice = int(input())
                    except ValueError:
                        print('Valor Incorreto')
                        continue
                    if choice == 0:
                        print(automatos[maquina] == automatos[maquina2])
                    elif choice == 1:
                        indice_maquina = indice_maquina + 1
                        automatos.append(automatos[maquina].multi_auto(automatos[maquina2]))
                        print('Sucesso')
                    elif choice == 2:
                        indice_maquina = indice_maquina + 1
                        automatos.append(automatos[maquina].union_automato(automatos[maquina2]))
                        print('Sucesso')
                    elif choice == 3:
                        indice_maquina = indice_maquina + 1
                        automatos.append(automatos[maquina].intercect_automato(automatos[maquina2]))
                        print('Sucesso')
                    elif choice == 4:
                        indice_maquina = indice_maquina + 1
                        automatos.append(automatos[maquina].difere_automato(automatos[maquina2]))
                elif choice == 12:
                    diretorio = input('Informe o diretorio : ')
                    if inout.salve_jff(automatos[maquina], diretorio):
                        print('Sucesso')
                elif choice == 14:
                    estado = input('Informe o estado a ser adicionado: ')
                    if automatos[maquina].set_new_states(estado):
                        print('Sucesso')
                    else:
                        print('ERRO')
                elif choice == 15:
                    caracter = input('Informe a nova letra a ser adicionado: ')
                    if automatos[maquina].set_new_alphabet(caracter):
                        print('Sucesso')
                    else:
                        print('ERROR')
                elif choice == 16:
                    source = input('Informe o estado source: ')
                    target = input('Informe o estado target: ')
                    consume = input('Informe o caracter de movimentacao: ')
                    if automatos[maquina].set_new_transition(source, target, consume):
                        print('Sucesso')
                    else:
                        print('ERROR')
                elif choice == 17:
                    estado = input('Informe a novo estado a ser inicial: ')
                    if automatos[maquina].set_new_start_state(estado):
                        print('Sucesso')
                    else:
                        print('ERROR')
                elif choice == 18:
                    estado = input('Informe a novo estado a ser final: ')
                    if automatos[maquina].set_new_final_state(estado):
                        print('Sucesso')
                    else:
                        print('ERROR')
                elif choice == 19:
                    estado = input('Informe o estado a ser removido: ')
                    if automatos[maquina].delete_state(estado):
                        print('Sucesso')
                    else:
                        print('ERRO')
                elif choice == 20:
                    caracter = input('Informe a  letra a ser removido: ')
                    if automatos[maquina].delete_alphabet(caracter):
                        print('Sucesso')
                    else:
                        print('ERROR')
                elif choice == 21:
                    source = input('Informe o estado source: ')
                    target = input('Informe o estado target: ')
                    consume = input('Informe o caracter de movimentacao: ')
                    if automatos[maquina].delete_transition(source, target, consume):
                        print('Sucesso')
                    else:
                        print('ERROR')
                elif choice == 22:
                    estado = input('Informe o estado a ser removido como inicial: ')
                    if automatos[maquina].delete_start_state(estado):
                        print('Sucesso')
                    else:
                        print('ERROR')
                elif choice == 23:
                    estado = input('Informe o estado a ser removido como final: ')
                    if automatos[maquina].delete_final_state(estado):
                        print('Sucesso')
                    else:
                        print('ERROR')

                input('Prescione enter para continuar')


if __name__ == "__main__":
    Main.main()
