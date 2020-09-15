from pychai.classes import UnitChar
class Selector():
    def __init__(self, sieves):
        self.sieves = sieves

    def __call__(self, unitChar: UnitChar) -> None:
        print(unitChar.name)
        for k,v in unitChar.powerDict.items():
            if v:
                print("----%s:%s"%(bin(k),v.name))
        possibleSchemeStrList = []
        for list_ in unitChar.possibleSchemeList:
            possibleSchemeStrList.append(''.join(["{%s}"%unitChar.powerDict[x].name for x in list_]))
        print("可行拆分：%s" % possibleSchemeStrList)
        for sieveName,_callable in self.sieves.items() :
            # bestEval = min(sieve(char, scheme) for scheme in char.schemeList)
            # selectBoolean = lambda scheme: sieve(char, scheme) == bestEval
            # char.schemeList = list(filter(selectBoolean, char.schemeList))
            evalList = [_callable(unitChar, scheme) for scheme in unitChar.possibleSchemeList]
            bestEval = min(evalList)
            unitChar.possibleSchemeList = [x[0]
                for x in zip(unitChar.possibleSchemeList, evalList) if x[1] == bestEval]
            possibleSchemeStrList = []
            for list_ in unitChar.possibleSchemeList:
                possibleSchemeStrList.append(''.join(["{%s}"%unitChar.powerDict[x].name for x in list_]))
            print("%s，结果：%s" % (sieveName,possibleSchemeStrList))
        print()
        # 理论上经过选择器序贯处理后应该只剩下一个 scheme。如果不是这样，报错
        if len(unitChar.possibleSchemeList) == 1:
            # 理论上把字根的二进制表示放进去才完备，但除了 C 输入要用到之外都不用，先不写
            # return tuple(
            #     {
            #         'name': char.powerDict[x],
            #         'slice': x
            #     }
            #     for x in char.schemeList[0])
            unitChar.scheme = tuple(unitChar.powerDict[x] for x in unitChar.possibleSchemeList[0])
        else:
            raise ValueError('您提供的拆分规则不能唯一确定拆分结果。例如，字「%s」有如下拆分方式：%s' \
                % (unitChar.name, unitChar.possibleSchemeList))