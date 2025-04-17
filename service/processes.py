'''Processes service'''

from siimm.siimm import ProcessData

def get_num_caracteres_automatico() -> int:
    """Detecta automaticamente o número de caracteres do processo no arquivo"""
    try:
        # Abrindo o arquivo para ler as linhas
        with open(file='Lista processos.txt', mode='r', encoding='utf8') as processes_list:
            processes = processes_list.readlines()

        # Usando a última linha como referência para determinar o número de caracteres do processo
        if processes:
            last_line = processes[-1].strip()  # Remover espaços extras
            # Vamos assumir que o número de caracteres do processo está no final da linha
            # Aqui é onde você pode ajustar, dependendo do formato do arquivo
            num_caracteres_processo = len(last_line.split()[-1])  # Considera o último "campo" como o número do processo
            return num_caracteres_processo
        else:
            raise ValueError("O arquivo está vazio ou mal formatado.")
    except Exception as e:
        print(f"Erro ao detectar o número de caracteres do processo: {e}")
        return 6  # Valor padrão caso haja erro

def get_all_processes(numero_secretaria, ano) -> list:
    '''Get all processes data'''
    num_caracteres_processo = get_num_caracteres_automatico()  # Detecta o número automaticamente

    with open(file='Lista processos.txt', mode='r', encoding='utf8') as processes_list:
        processes = processes_list.readlines()

    processes_number_list = []
    for process in processes:
        # Pega os últimos 'num_caracteres_processo' caracteres de cada linha
        process_number = process.strip()[-num_caracteres_processo:]
        processes_number_list.append(process_number)

    for process_number in processes_number_list:
        ProcessData(numero_processo=process_number, numero_secretaria=numero_secretaria, ano=ano).get_process_data()

    return processes_number_list
