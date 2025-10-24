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

    # Transforms pattern into checks for literals
    def expressionToMatchPattern(self, exp, mainValue, checks = []):
        # Object pattern match:

        if exp['type'] == 'ObjectExpression':
            for property in exp['properties']:
                if property['value']['type'] == 'Identifier':
                    break

                if property['value']['type'] == 'NumericLiteral' or property['value']['type'] == 'StringLiteral':
                    checks.append(self._createPropCompare(property))
                # Nested
                elif property['value']['type'] == 'ObjectExpression':
                    self.expressionToMatchPattern(property['value'], mainValue, checks)

            ifNode = self._createIfTest(checks)
            return [exp, ifNode]

        # Simple literal match:
        elif exp['type'] == 'NumercLiteral' or exp['type'] == 'StringLiteral':
            checks.append(self._createValueCompare(exp, mainValue))

            ifNode = self._createIfTest(checks)

            return [None, ifNode]

        # Identifier match:
        elif exp['type'] == 'Identifier':
            return [None, None]

        raise Exception(f"no match type: {type}")

    # Creates property comparison.
    def _createPropCompare(self, property):
        expected = property['value']

        binding = {
            'type': 'Identifier',
            'name': f"_{property['key']['name']}"
        }

        property['value'] = binding

        return self._createValueCompare(binding ,expected)

    # Creates value comparison.
    def _createValueCompare(self, exp, expected):
        return {
            'type': 'BinaryExpression',
            'left': exp,
            'operator': '!=',
            'right': expected,
        }

    # Creates if-test for pattern value.
    def _createIfTest(self, checks):
        ifCond = checks[0]

        i = 1

        while i < len(checks):
            ifCond = {
                'type': 'LogicalExpression',
                'left': ifCond,
                'operator': '||',
                'right': checks[i]
            }
            i = i + 1

        return {
            'type': 'IfStatement',
            'test': ifCond,
            'consequent': {
                'type': 'ThrowStatement',
                'argument': {
                    'type': 'Identifier',
                    'name': 'NextMatch',
                }
            }
        }



