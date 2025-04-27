import re
import subprocess
from threading import Thread
from queue import Queue, Empty

progress = {}


def parse_rclone_progress(line, progress):
    """Extrai os dados de progresso da saída do Rclone."""
    patterns = {
        'transferred': r'Transferred:\s+([\d.]+\s*\w+)\s*\/\s*([\d.]+\s*\w+)',
        'speed': r'([\d.]+\s*\w+\/s)',
        'eta': r'ETA\s+([^-]+)',
        'checks': r'Checks:\s+(\d+)\s*\/\s*(\d+)',
        'elapsed': r'Elapsed time:\s+([\d.]+[hms]*)'
    }
    # progress = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, line)

        if match:
            if key == 'transferred':
                progress['transferred_bytes'] = match.group(1)
                progress['total_bytes'] = match.group(2)
            elif key == 'checks':
                progress['checks_done'] = match.group(1)
                progress['checks_total'] = match.group(2)
            else:
                progress[key] = match.group(1)
    return progress

def read_output(pipe, queue):
    """Lê a saída do subprocesso linha por linha e coloca na fila."""
    for line in iter(pipe.readline, ''):
        queue.put(line)
    pipe.close()

def run_rclone_with_progress(command, progress):
    """Executa o comando Rclone e retorna o progresso em tempo real."""
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        shell=True
    )
    
    queue = Queue()
    thread = Thread(target=read_output, args=(process.stdout, queue))
    thread.daemon = True
    thread.start()
    
    try:
        while True:
            try:
                line = queue.get(timeout=0.1)
                if line is None:  # Sinal de término
                    break
                    
                if 'Transferred:' in line or 'Checks:' in line or 'Elapsed time:' in line:
                    progress = parse_rclone_progress(line, progress)
                    transferred = progress.get('transferred_bytes', 'Nada')
                    speed = progress.get('speed', 'Nada')
                    time = progress.get('elapsed', 'Nada')
                    print(f"Transferido: {transferred}, Velocidade: {speed}, Tempo: {time}")
                    
                # print(line.strip(), '\n')
            except Empty:
                if process.poll() is not None:  # Processo terminou
                    break
    finally:
        thread.join(timeout=1)
        if process.poll() is None:  # Se ainda estiver rodando
            process.terminate()
            process.wait()

# Exemplo de uso
if __name__ == "__main__":
    rclone_command = './rclone copy drive1: /home/andravi/TesteRclone/ -P'
    exit_code = run_rclone_with_progress(rclone_command, progress)
    print("Processo finalizado com código:", exit_code)
