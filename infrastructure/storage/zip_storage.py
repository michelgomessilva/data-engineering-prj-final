import os
import zipfile
from datetime import datetime
from pathlib import Path
from typing import List


class ZipExtractor:
    """
    Classe utilitária para descompactar arquivos ZIP.

    Responsável por extrair todos os arquivos de um zip para um diretório específico
    e retornar a lista de caminhos extraídos.
    """

    @staticmethod
    def extract_all(zip_path: str, extract_dir: str) -> List[str]:
        """
        Extrai todos os arquivos de um arquivo ZIP.

        Args:
            zip_path (str): Caminho completo para o arquivo .zip.
            extract_dir (str): Caminho do diretório onde os arquivos serão extraídos.

        Returns:
            List[str]: Lista de caminhos completos dos arquivos extraídos.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        extract_dir = f"{extract_dir}-{timestamp}"

        if not os.path.exists(extract_dir):
            os.makedirs(extract_dir)

        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extract_dir)
            extracted_files = [
                os.path.join(extract_dir, name) for name in zip_ref.namelist()
            ]

        return extracted_files

    @staticmethod
    def is_file_larger_than_32mb(file_path: str) -> bool:
        """
        Verifica se o arquivo é maior que 32 megabytes.

        Args:
            file_path (str): Caminho completo do arquivo.

        Returns:
            bool: True se for maior que 32MB, False caso contrário.
        """
        size_in_bytes = os.path.getsize(file_path)
        return size_in_bytes > 32 * 1024 * 1024  # 32 MB em bytes

    @staticmethod
    def split_file_by_size(
        input_file: str, output_dir: str, max_size_mb: int = 32
    ) -> list[str]:
        """
        Divide um arquivo em múltiplos arquivos de no máximo `max_size_mb` MB,
        garantindo que as linhas não sejam cortadas no meio e mantendo o cabeçalho em cada parte.

        Args:
            input_file (str): Caminho do arquivo original.
            output_dir (str): Diretório onde os arquivos divididos serão salvos.
            max_size_mb (int): Tamanho máximo de cada arquivo (em MB).

        Returns:
            list[str]: Lista com os caminhos dos arquivos criados.
        """
        os.makedirs(output_dir, exist_ok=True)

        part_files = []
        max_bytes = max_size_mb * 1024 * 1024  # converte MB para bytes
        part_index = 1
        current_size = 0
        current_lines = []

        def write_part(lines, index):
            filename = Path(input_file).stem
            part_path = os.path.join(output_dir, f"{filename}_part_{index:03d}.txt")
            with open(part_path, "w", encoding="utf-8") as f:
                f.writelines(lines)
            return part_path

        with open(input_file, "r", encoding="utf-8") as infile:
            header = infile.readline()
            header_size = len(header.encode("utf-8"))
            if not header.strip():
                raise ValueError("Arquivo de entrada vazio ou sem cabeçalho.")

            current_lines.append(header)
            current_size += header_size

            for line in infile:
                line_size = len(line.encode("utf-8"))

                # se a próxima linha ultrapassar o limite, escreve o atual
                if current_size + line_size > max_bytes:
                    part_file = write_part(current_lines, part_index)
                    part_files.append(part_file)
                    part_index += 1
                    current_lines = [header]  # reinicia com cabeçalho
                    current_size = header_size

                current_lines.append(line)
                current_size += line_size

            # salva o último pedaço restante
            if len(current_lines) > 1:  # se tem mais que só o cabeçalho
                part_file = write_part(current_lines, part_index)
                part_files.append(part_file)

        return part_files
