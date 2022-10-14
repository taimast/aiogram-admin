import psutil as psutil


def main():
    for process in psutil.process_iter():
        if process.name() == 'pytest.exe':
            process.terminate()
            print('Process terminated')


if __name__ == '__main__':
    main()
