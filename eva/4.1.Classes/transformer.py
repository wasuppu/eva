# AST Transformer.
class Transformer:
    '''
    Translates `def`-expression (function declaration)
    into a variable declaration with a lambda expression
    '''
    def transformDefToVarLambda(self, defExp):
        _tag, name, params, body = defExp
        return ['var', name, ['lambda', params, body]]

    # Transforms `switch` to nested `if`-expressions.
    def transformSwitchToIf(self, switchExp):
        [_tag, *cases] = switchExp

        ifExp = ['if', None, None, None]
        current = ifExp
        for i in range(len(cases) - 1):
            current[1], current[2] = cases[i]

            next = cases[i+1]
            nextCond, nextBlock = next

            if nextCond == 'else':
                if i != len(cases) - 2:
                    raise Exception("bad syntax (`else' clause must be last)")
                current[3] = nextBlock
                break
            else:
                current[3] = ['if', None, None, None]

            current = current[3]

        return ifExp

    def transformForToWhile(self, forExp):
        [_tag, init, cond, mod, exp] = forExp
        return ['begin', init, ['while', cond, ['begin', exp, mod]]]

    def transformIncToSet(self, exp):
        _tag, name = exp
        setExp = ['set', name, ['+', name, 1]]
        return setExp

    def transformDecToSet(self, exp):
        _tag, name = exp
        setExp = ['set', name, ['-', name, 1]]
        return setExp

    def transformIncValToSet(self, exp):
        _tag, name, val = exp
        setExp = ['set', name, ['+', name, val]]
        return setExp

    def transformDecValToSet(self, exp):
        _tag, name, val = exp
        setExp = ['set', name, ['-', name, val]]
        return setExp

    def transformMulValToSet(self, exp):
        _tag, name, val = exp
        setExp = ['set', name, ['*', name, val]]
        return setExp

    def transformDivValToSet(self, exp):
        _tag, name, val = exp
        setExp = ['set', name, ['/', name, val]]
        return setExp