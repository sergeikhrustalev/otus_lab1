import ast
import os
import collections

from nltk import pos_tag


def flat(_list):
    """ [(1,2), (3,4)] -> [1, 2, 3, 4]"""
    return sum([list(item) for item in _list], [])


def is_verb(word):
    if not word:
        return False
    pos_info = pos_tag([word])
    return pos_info[0][1] == 'VB'


def get_tree(filename):
    with open(filename) as file_handler:
        main_file_content = file_handler.read()
    try:
        return ast.parse(main_file_content)
    except SyntaxError as e:
        print('ERROR: ', e)


def get_python_code_filenames(path, max_filenames=100):
    filenames = []
    for dirname, dirs, files in os.walk(path, topdown=True):
        for file in files:
            if file.endswith('.py'):
                filenames.append(os.path.join(dirname, file))
                if len(filenames) == max_filenames:
                    break
    return filenames


def get_trees(filenames):
    trees = []
    for filename in filenames:
        tree = get_tree(filename)
        if tree is not None:
            trees.append(tree)
    return trees


def get_functions_from_trees(trees):
    return [f for f in flat([[node.name.lower() for node in ast.walk(t) if isinstance(node, ast.FunctionDef)] for t in trees]) if not (f.startswith('__') and f.endswith('__'))]


def get_verbs_from_function_name(function_name):
    return [word for word in function_name.split('_') if is_verb(word)]


def get_top_verbs_in_functions(functions, top_size=10):
    verbs = flat([get_verbs_from_function_name(function_name) for function_name in functions])
    return collections.Counter(verbs).most_common(top_size)


wds = []
projects = [
    'django',
    'flask',
    'pyramid',
    'reddit',
    'requests',
    'sqlalchemy',
]
for project in projects:
    path = os.path.join('.', project)
    filenames = get_python_code_filenames(path)
    print('total %s files' % len(filenames))
    trees = get_trees(filenames)
    print('trees generated')
    functions = get_functions_from_trees(trees)
    print('functions extracted')
    wds += get_top_verbs_in_functions(functions)

top_size = 200
print('total %s words, %s unique' % (len(wds), len(set(wds))))
for word, occurence in collections.Counter(wds).most_common(top_size):
    print(word, occurence)
