import os
import main_wrapper


def clean_dir(directory: str, ext: str):
    for file in os.listdir(directory):
        if file.endswith(ext):
            os.remove(os.path.join(directory, file))
            print("file {} have been removed".format(file))


def clean():
    current_dir = os.path.dirname(__file__)
    output_dir = os.path.join(current_dir, 'output')
    clean_dir(output_dir, '.png')
    for fn in os.listdir(output_dir):
        fn_full = os.path.join(output_dir, fn)
        if os.path.isdir(fn_full):
            if fn in main_wrapper.main_nuclides:
                clean_dir(fn_full, '.dat')


if __name__ == '__main__':
    clean()

