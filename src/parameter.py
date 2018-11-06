from abc import ABC

g_lesHouchesBlocks = {}

class LesHouchesBlock :
    def __init__ (self, name) :
        """
        Parameters
        ----------
        name: str
          A name for this block
        """
        self.name = name
        g_lesHouchesBlocks[name] = self
        self.externParamsByOrderBlock = {} # dictionary indexes are block nbrs
        self.orderBlock = 1

    def insertExternParam (self, param) :
        """
        Parameters
        ----------
        param: InternParam based class instance
          The internal parameter to insert into this block
        """
        if param.orderBlock is not None :
            if param.orderBlock in self.externParamsByOrderBlock :
                raise ValueError('Cannot insert duplicate external param %s' % param)

            self.externParamsByOrderBlock[param.orderBlock] = param
        else :
            # Find unused order block
            while self.orderBlock in self.externParamsByOrderBlock :
                self.orderBlock += 1
            self.externParamsByOrderBlock[self.orderBlock] = param

class PyRuleParam (ABC) :
    """
    Abstract base class for external and internal parameter instances.
    """

    def __init__ (self,
        interactionOrder) :
        """
        Parameters
        ----------
        interactionOrder: 2-tuple (str, number) or array of 2-tuples
          Specifies the order of the parameter according to a specific interaction. 
          It refers to a pair with the interaction name, followed by the order, or a list of such pairs.
        """

        self.interactionOrder = interactionOrder

class ExternParam (PyRuleParam) :
    """
    External parameter
l    """
    def __init__ (self, 
      value = 1.0, # Real number
      blockName = 'FRBlock',
      interactionOrder = None,
      orderBlock = None) :

      """
      Parameters
      ----------
      value: floating point number
        The real number value to assign to this parameter.
      blockName: str
        The name identifying the block associated with this parameter
      interactionOrder: 2-tuple (str, number)
        Specifies the order of the parameter according to a specific interaction. 
        It refers to a pair with the interaction name, followed by the order, or a list of such pairs.
      orderBlock: positive integer
        Provides information about the position of an external parameter within a given Les Houches block.
      """

      self.value = value
      self.orderBlock = orderBlock

      if blockName in g_lesHouchesBlocks :
        self.block = g_lesHouchesBlocks[blockName]
      else :
        self.block = LesHouchesBlock(blockName)
        g_lesHouchesBlocks[blockName] = self.block

      self.block.insertExternParam(self)

      super(ExternParam, self).__init__(interactionOrder)

    def __unicode__ (self) :
      return '{}[{}]: {}'.format(self.block.name,
        self.orderBlock,
        self.value)

class InternParam (PyRuleParam) :
    """
    Internal parameters can be either real or complex, and are connected to other parameters via an analytical formula.
    """
    def __init__ (self,
        value,
        complexParameter,
        interactionOrder = None, # A 2-tupe (ExternParam, order)
        parameterName = None) :
        """
        Parameters
        ----------
        value: str
          analytical formula defining the parameter that can be expressed in terms of other parameters.
        complexParameter: bool
          Parameter is a complex quantity if True, or a real value if False.
        interactionOrder: 2-tuple
          Specifies the order of the parameter according to a specific interaction. 
          It refers to a pair with the interaction name, followed by the order, or a list of such pairs.
        parameterName: str
          Specifies what to replace the symbol by before writing out the Feynman diagram calculator model files. By default, it is taken equal to the symbol representing the parameter.
        """

        self.value = value
        self.complexParameter = complexParameter
        self.parameterName = parameterName
        super(InternParam, self).__init__(interactionOrder)

class ExternTensorParam (ExternParam) :
    """
    Tensorial external parameter.
    """
    def __init__ (self,
        indices,
        value,
        blockName = 'FRBlock',
        orderBlock = None,
        complexParameter = True,
        interactionOrder = None, # A 2-tupe (ExternParam, order)
        unitary = False,
        hermitian = False,
        orthogonal = False,
        allowSummation = False) :

        """
        Parameters
        ----------
        indices: Array of strings
            An array of index types. E.g ['scalar', 'generation']
        value: numpy.matrix
            The tensor values
        complexParameter: bool
          Defines whether the parameter is a real (False) or complex (True) quantity.
        interactionOrder: 2-tuple (str, number) or array of 2-tuples
          Specifies the order of the parameter according to a specific interaction. 
          It refers to a pair with the interaction name, followed by the order, or a list of such pairs.
        unitary: bool
          True if parameter corresponds to unitary matrix
        hermitian: bool
          True if parameter corresponds to Hermitian matrix
        orthogonal: bool
          True if parameter corresponds to orthogonal matrix
        allowSummation: bool
        """

        self.indices = indices
        self.complexParameter = complexParameter
        self.unitary = unitary
        self.hermitian = hermitian
        self.orthogonal = orthogonal
        self.allowSummation = allowSummation

        super(ExternTensorParam, self).__init__(value, 
          blockName,
          interactionOrder,
          orderBlock)

class InternTensorParam (ExternParam) :
    """
    Tensorial internal parameter.
    """
    def __init__ (self,
        indices,
        value,
        complexParameter = True,
        interactionOrder = None, # A 2-tupe (ExternParam, order)
        parameterName = None,
        unitary = False,
        hermitian = False,
        orthogonal = False,
        allowSummation = False) :

        """
        Parameters
        ----------
        indices: A list of index types. E.g ['scalar', 'generation']
        value: numpy.matrix
            The tensor values
        complexParameter: bool
          Defines whether a parameter is a real (False) or complex (True) quantity.
        interactionOrder: 2-tuple (str, number) or array of 2-tuples
          Specifies the order of the parameter according to a specific interaction. 
          It refers to a pair with the interaction name, followed by the order, or a list of such pairs.
        parameterName: str
          Specifies what to replace the symbol by before writing out the Feynman diagram calculator model files. By default, it is taken equal to the symbol representing the parameter.
        unitary: bool
          True if parameter corresponds to unitary matrix
        hermitian: bool
          True if parameter corresponds to Hermitian matrix
        orthogonal: bool
          True if parameter corresponds to orthogonal matrix
        allowSummation: bool
        """

        self.indices = indices
        self.unitary = unitary
        self.hermitian = hermitian
        self.orthogonal = orthogonal
        self.allowSummation = allowSummation

        super(InternTensorParam, self).__init__(value, 
          complexParameter,
          interactionOrder,
          parameterName)
