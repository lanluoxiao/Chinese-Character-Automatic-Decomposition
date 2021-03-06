常用模板类
===========================

顺序模板类（``core.Sequential``）
---------------------------------

**定义**\ （笔画列表）部件 :math:`c` 所包含的笔画形成的序列
:math:`\operatorname{str}c=(s_1,s_2,\cdots,s_n)`\ 。

**定义**\ （切片）设部件 :math:`c` 的笔画列表的长度为
:math:`n`\ ，我们指定一组指标 :math:`i_1,\cdots,i_n` 使得

.. math::


   1\le i_1\le\cdots\le i_n\le n

那么由第 :math:`i_1,\cdots,i_n`
个笔画在平面上按此顺序在原有位置上排布组成的几何图形称为一个切片。

我们将切片记为 :math:`p_i=c[i_1,\cdots,i_n]`\ 。显然，它的笔画序列为

.. math::


   \operatorname{str}(c[i_1,\cdots,i_n])=(s_{i_1},\cdots,s_{i_n})

**定义**\ （部件的拆分）给定部件 :math:`c`\ ，我们称由 :math:`k` 个
:math:`c` 的切片构成的 :math:`k` 元组 :math:`d=(p_1,\cdots,p_k)`
是一个拆分，当且仅当任两个切片无共同笔画，且所有切片所含的笔画的并集等于汉字
:math:`c` 的所有笔画。

**定义**\ （部件的拆分集）给定汉字 :math:`c`\ ，由所有可能拆分 :math:`d`
构成的集合 :math:`D`\ 。


退化映射（\ ``base.degenerator.Degenerator``\ ）

根据架构，我们首先需要将基本部件拆分为字根。但是，当我们利用上述坐标数据时，我们就面临着一个问题：用户可能希望将不同的字中不同的切片视为同一字根，尽管这些切片的坐标数据不完全一样。例如，「串」中的两个「口」上面的小、下面的大，坐标数据并不相同，但通常用户会将其看作同一字根。如何实现呢？

一种思路是，直接利用上述全部信息，结合人工智能的分类方法进行分类。然而，这将会花费巨大的运算资源（例如，请了解手写数字的神经网络分类模型），于是我们思考的是，上述信息中是否存在某些简单、信息量少的「关键部分」，使得我们仅通过这些关键部分就能有效的区分不同字根？

「拆」为此进行了尝试，将这种对一个切片提取关键信息的函数称为「退化映射」，得到的关键信息称之为「特征」。这样，我们将一个切片经退化映射处理，得到的特征与字根的特征进行比较，如果它的特征与某个字根的特征相等，就可以将它等同于该字根。相反，如果它不与任何字根的特征相等，它就是一个无效切片，不能作为拆分的一部分。

**定义**\ （退化映射）\ :math:`\mathcal O`
将一个切片或一个字根映射为含有较少信息的对象，且满足：

.. math::


   \forall r_1,r_2\in R,r_1\ne r_2\Rightarrow \mathcal O(r_1)\ne \mathcal O(r_2)

即 :math:`\mathcal O` 在字根集 :math:`R` 上是单射。

**定义**\ （部件的可行拆分集）给定汉字 :math:`c`\ ，它的拆分集是
:math:`D`\ ，则它的可行拆分集 :math:`W` 定义为：

.. math::


   W=\{d|d\in D;\forall p\in d, \exists r\in R\text{ s.t. }\mathcal O(r)=\mathcal O(p)\}

即：对于该拆分中的每一个切片，都存在一个字根使得该字根退化后得到的对象与该切片退化后得到的对象一致。

在实际操作中，我们可能会提取多种不同的关键信息，然后将它们组合起来成为一个字的特征。此时每种信息称为一个「域（field）」，生成这个域的函数称为域函数。

为了便于查询，我们计算所有字根的特征，形成一个以特征索引用户字根的字典；此后，每当我们获得了一个基本部件的切片，我们就能取其特征并在字典中查找，查找得到则为有效切片，否则为无效切片。


依次调用上述三个方法，并把得到的码表保存到给定路径下。

顺序中间类（\ ``core.sequential.Sequential``\ ）
------------------------------------------------

幂字典生成（\ ``Sequential.__addPowerDict``\ ）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

我们现在讨论：给定一个基本部件，我们可以从其中拆出哪些字根？为了满足不同方案的需求，「拆」采用了比较激进的方案——枚举一个基本部件的所有切片，计算该切片的特征，然后在退化字典中查找它所对应的字根，如果能够找到则标记为有效切片，找不到则标记为无效切片。

那么，一个基本部件最多能形成多少种切片？显然，对于一个 n
笔的字，每个笔画都有取和不取两种状态，因而切片就有 2 的 n
次方种可能性。我们因此可以用 n 个布尔值（即 0 或
1）组成的向量来表达这一切片。例如：

-  设字 c 是含有 5 笔的字，则它的所有切片都可以用一个\ **含有 5
   个布尔值的向量**\ 表达；
-  取字 c 前 2 笔和最后一笔作为一个切片 s，我们对每个笔画将「取」标记为
   1，「不取」标记为 0，那么 s 对应的向量应该是 (1, 1, 0, 0, 1)；
-  取完切片 s 之后，余下部分 r 对应的向量应该是 (0, 0, 1, 1, 0)。

进一步抽象之后，我们很自然地联想到可以使用二进制数来表达切片，这样的好处是我们可以通过位运算来快速处理切片。例如：

-  设字 c 是含有 5 笔的字，则它的所有切片都可以用一个\ **含有 5
   个位的二进制数**\ 表达；
-  取字 c 前 2 笔作为一个切片 s，我们对每个笔画将「取」标记为
   1，「不取」标记为 0，那么 s 对应的二进制数应该是
   11001，转换为十进制数是 25；
-  取完切片 s 之后，余下部分 r 对应的向量应该是 00111，转换为十进制数是
   6。

现在，我们就可以通过遍历 1 ~ 2n-1 的所有数字来寻找一个字的所有有效切片：

现在，幂字典中记录了每个切片分别对应哪个字根（或者不对应任何字根），由此我们可以正式进入一个字的拆分环节。

可行拆分集生成（\ ``Sequential.__addSchemeList``\ ）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

在未开始拆分之前，我们将一个字的状态用 2n-1
表示，我们将它称为剩余数。每当我们从这个字上取下一个切片时，我们就将这个切片对应的数从剩余数中减去，得到新的剩余数。那么给定任意一个剩余数，我们如何知道从它身上能取下哪些切片呢？

首先，我们要引入一个限定原则（首笔序原则），即拆分得到的字根列表是按它们首笔笔顺排列的。因此，在每次从没有拆完的部分中取切片的过程中，必须取到该部分的第一笔。例如，第一次拆分时必须取到该字的第一笔。

所以，拆分算法可以概括为：

-  建立两个列表记录拆分状态，一个为未完成列表，一个为完成列表，向未完成列表中加入初始值
   (2n - 1)，即将整个部件作为一个剩余数；
-  取未完成列表中的某个拆分，将它的最后一个数（即剩余数）经由
   ``nextRoot``
   函数处理，得到所有可能切片，用幂字典检验它们的有效性，如果无效则予以剔除，有效则保留；
-  如果切片恰好等于剩余数，说明这个基本部件被拆完了，我们将它添加到已完成列表中；否则用剩余数减去新切片，将它添加到未完成列表中，形成堆栈；
-  重复上述过程，直到未完成列表全部被清空。
