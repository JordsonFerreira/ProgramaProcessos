from datetime import datetime
import os
import json
import pandas as pd
import load
from .processes import get_all_processes

def create_updated_dataframe(numero_secretaria, ano) -> str:
    """Main function for creating the updated dataframe."""
    # Obtemos a lista de processos
    processes_number_list = get_all_processes(numero_secretaria, ano)

    # Define o diretório base e garante que ele exista
    base_directory = f"data/{datetime.now().strftime('%Y-%m-%d')}"
    directory = load.create_directory_if_not_exists(base_directory)

    # Carregamos a tabela de processos
    processes_table = pd.read_excel('Processos.xlsx')

    for process_number in processes_number_list:
        process_number = str(process_number).strip()  # Remove espaços ou tabulações
        file = os.path.join(directory, f'{process_number}.json')

        try:
            with open(
                file=file,
                mode="r",
                encoding="utf8"
            ) as f:
                data = json.load(f)

            if 'data' not in data or not data['data']:
                print(f"No data found for process {process_number}. Skipping.")
                continue

            # Extraímos as datas
            date = data['data'][-1].get('data', "")
            if date == "":
                if len(data['data']) > 1:
                    date = data['data'][-2].get('data', "")
                else:
                    print(f"No valid date found for process {process_number}. Skipping.")
                    continue

            date_now = datetime.now().strftime('%d/%m/%Y')
            updated_date = datetime.strptime(date_now, "%d/%m/%Y")
            last_date = datetime.strptime(date, "%d/%m/%Y")
            sector_period = (updated_date - last_date).days

            process_opening = data['data'][0].get('data', "")
            opening_date = datetime.strptime(process_opening, "%d/%m/%Y")
            total_period = (updated_date - opening_date).days

            # Atualizamos as colunas da tabela
            processes_table.loc[processes_table['PROCESSO']
                                == int(process_number), 'ABERTURA DO PROCESSO'] = process_opening
            processes_table.loc[processes_table['PROCESSO']
                                == int(process_number), 'ATUALIZAÇÃO'] = date
            processes_table.loc[processes_table['PROCESSO']
                                == int(process_number), 'STATUS'] = data['data'][-1].get('setor', "")
            processes_table.loc[processes_table['PROCESSO']
                                == int(process_number), 'PERÍODO QUE ENCONTRA-SE NO SETOR (DIAS)'] = sector_period
            processes_table.loc[processes_table['PROCESSO']
                                == int(process_number), 'PERÍODO TOTAL DESDE A ABERTURA (DIAS)'] = total_period

        except Exception as e:
            print(f"Erro ao processar o processo {process_number}: {e}")
            continue

    # Define o nome do arquivo com base na data atual
    base_filename = f"processosAtualizados{datetime.now().strftime('%Y-%m-%d')}"
    final_filename = os.path.join(directory, f"{base_filename}.xlsx")

    # Verifica se já existe um arquivo com o mesmo nome e incrementa o índice se necessário
    counter = 1
    while os.path.exists(final_filename):
        final_filename = os.path.join(directory, f"{base_filename} ({counter}).xlsx")
        counter += 1

    # Salva o arquivo final após o loop
    processes_table.to_excel(final_filename, index=False)
    print(f'Processos atualizados e salvos em {final_filename}!')

    return final_filename  # Retorna o nome do arquivo gerado
