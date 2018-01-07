import ast
import os
import collections

from nltk import pos_tag


def flat_list(multiple_list):
    return sum(multiple_list, [])


def is_verb(word):
    if not word:
        return False
    pos_info = pos_tag([word])
    return pos_info[0][1] == 'VB'


def get_content_from_file(filename):
    with open(filename) as file_handler:
        return file_handler.read()


def get_ast_tree(content):
    try:
        return ast.parse(content)
    except SyntaxError as error:
        print(error)


def get_python_code_filenames(path, max_filenames=100):
    filenames = []
    for dirname, dirs, files in os.walk(path, topdown=True):
        for file in files:
            if file.endswith('.py'):
                filenames.append(os.path.join(dirname, file))
                if len(filenames) == max_filenames:
                    break
    return filenames


def get_contents_from_files(filenames):
    return [get_content_from_file(filename) for filename in filenames]


def get_ast_trees(contents):
    return [
        tree
        for tree in [get_ast_tree(content) for content in contents]
        if tree
    ]


def get_typical_function_names(trees):
    func_names = flat_list(
        [
            [
                node.name.lower()
                for node in ast.walk(tree)
                if isinstance(node, ast.FunctionDef)
            ]
            for tree in trees
        ]
    )
    return [
        func
        for func in func_names
        if not (func.startswith('__') and func.endswith('__'))
    ]


def get_verbs_from_function_name(function_name):
    return [word for word in function_name.split('_') if is_verb(word)]


def get_top_verbs_in_function_names(function_names, top_size=10):
    verbs = flat_list(
        [get_verbs_from_function_name(name) for name in function_names]
    )
    return collections.Counter(verbs).most_common(top_size)


def get_top_words(words, top_size=200):
    return collections.Counter(words).most_common(top_size)


if __name__ == '__main__':
    words = []

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
        print('total {} files'.format(len(filenames)))
        contents = get_contents_from_files(filenames)
        trees = get_ast_trees(contents)
        print('trees generated')
        function_names = get_typical_function_names(trees)
        print('functions extracted')
        words += get_top_verbs_in_function_names(function_names)

    print('total {} words, {} unique'.format(len(words), len(set(words))))
    for word, occurence in get_top_words(words):
        print(word, occurence)
