# JS Transform.
class JSTransform:
    # Transforms normal function to an async generator.
    def functionToAsyncGenerator(self, fnNode):
        genFn = {
            'type': 'FunctionDeclaration',
            'id': {
                'type': 'Identifier',
                'name': f"_{fnNode['id']['name']}",
            },
            'generator': True,
            'async': True,
            'params': fnNode['params'],
        }

        fnBlock = fnNode['body']
        genBlockBody = fnBlock['body'].copy()

        for i in range(1, len(genBlockBody), 2):
            genBlockBody.insert(i, {
                'type': 'ExpressionStatement',
                'expression': {
                    'type': 'YieldExpression'
                }
            })

        genFn['body'] = {
            'type': 'BlockStatement',
            'body': genBlockBody,
        }

        return genFn

