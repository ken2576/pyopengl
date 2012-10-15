'''OpenGL extension ARB.shader_objects

This module customises the behaviour of the 
OpenGL.raw.GL.ARB.shader_objects to provide a more 
Python-friendly API

Overview (from the spec)
	
	This extension adds API calls that are necessary to manage shader
	objects and program objects as defined in the OpenGL 2.0 white papers by
	3Dlabs.
	
	The generation of an executable that runs on one of OpenGL's
	programmable units is modeled to that of developing a typical C/C++
	application. There are one or more source files, each of which are
	stored by OpenGL in a shader object. Each shader object (source file)
	needs to be compiled and attached to a program object. Once all shader
	objects are compiled successfully, the program object needs to be linked
	to produce an executable. This executable is part of the program object,
	and can now be loaded onto the programmable units to make it part of the
	current OpenGL state. Both the compile and link stages generate a text
	string that can be queried to get more information. This information
	could be, but is not limited to, compile errors, link errors,
	optimization hints, etc. Values for uniform variables, declared in a
	shader, can be set by the application and used to control a shader's
	behavior.
	
	This extension defines functions for creating shader objects and program
	objects, for compiling shader objects, for linking program objects, for
	attaching shader objects to program objects, and for using a program
	object as part of current state. Functions to load uniform values are
	also defined. Some house keeping functions, like deleting an object and
	querying object state, are also provided.
	
	Although this extension defines the API for creating shader objects, it
	does not define any specific types of shader objects. It is assumed that
	this extension will be implemented along with at least one such
	additional extension for creating a specific type of OpenGL 2.0 shader
	(e.g., the ARB_fragment_shader extension or the ARB_vertex_shader
	extension).

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/ARB/shader_objects.txt
'''
from OpenGL import platform, constants, constant, arrays
from OpenGL import extensions, wrapper
from OpenGL.GL import glget
import ctypes
from OpenGL.raw.GL.ARB.shader_objects import *
### END AUTOGENERATED SECTION
EXTENSION_NAME = 'GL_ARB_shader_objects'
import OpenGL
from OpenGL._bytes import bytes, _NULL_8_BYTE
from OpenGL.lazywrapper import lazy
from OpenGL import converters, error
GL_INFO_LOG_LENGTH_ARB = constant.Constant( 'GL_INFO_LOG_LENGTH_ARB', 0x8B84 )

glShaderSourceARB = platform.createExtensionFunction(
    'glShaderSourceARB', dll=platform.GL,
    resultType=None,
    argTypes=(constants.GLhandleARB, constants.GLsizei, ctypes.POINTER(ctypes.c_char_p), arrays.GLintArray,),
    doc = 'glShaderSourceARB( GLhandleARB(shaderObj), [bytes(string),...] ) -> None',
    argNames = ('shaderObj', 'count', 'string', 'length',),
    extension = EXTENSION_NAME,
)
conv = converters.StringLengths( name='string' )
glShaderSourceARB = wrapper.wrapper(
    glShaderSourceARB
).setPyConverter(
    'count' # number of strings
).setPyConverter(
    'length' # lengths of strings
).setPyConverter(
    'string', conv.stringArray
).setCResolver(
    'string', conv.stringArrayForC,
).setCConverter(
    'length', conv,
).setCConverter(
    'count', conv.totalCount,
)
try:
    del conv
except NameError as err:
    pass

for size in (1,2,3,4):
    for format,arrayType in (
        ('f',arrays.GLfloatArray),
        ('i',arrays.GLintArray),
    ):
        name = 'glUniform%(size)s%(format)svARB'%globals()
        globals()[name] = arrays.setInputArraySizeType(
            globals()[name],
            None, # don't want to enforce size...
            arrayType,
            'value',
        )
        try:
            del format, arrayType
        except NameError as err:
            pass
    try:
        del size
    except NameError as err:
        pass

@lazy( glGetObjectParameterivARB )
def glGetObjectParameterivARB( baseOperation, shader, pname ):
    """Retrieve the integer parameter for the given shader"""
    status = arrays.GLintArray.zeros( (1,))
    status[0] = 1
    baseOperation(
        shader, pname, status
    )
    return status[0]

@lazy( glGetObjectParameterfvARB )
def glGetObjectParameterfvARB( baseOperation, shader, pname ):
    """Retrieve the float parameter for the given shader"""
    status = arrays.GLfloatArray.zeros( (1,))
    status[0] = 1.0
    baseOperation(shader, pname,status)
    return status[0]

def _afterCheck( key ):
    """Generate an error-checking function for compilation operations"""
    def GLSLCheckError(
        result,
        baseOperation=None,
        cArguments=None,
        *args
    ):
        result = error.glCheckError( result, baseOperation, cArguments, *args )
        status = glGetObjectParameterivARB(
            cArguments[0], key
        )
        if not status:
            raise error.GLError(
                result = result,
                baseOperation = baseOperation,
                cArguments = cArguments,
                description= glGetInfoLogARB( cArguments[0] )
            )
        return result
    return GLSLCheckError

if OpenGL.ERROR_CHECKING:
    glCompileShaderARB.errcheck = _afterCheck( GL_OBJECT_COMPILE_STATUS_ARB )
if OpenGL.ERROR_CHECKING:
    glLinkProgramARB.errcheck = _afterCheck( GL_OBJECT_LINK_STATUS_ARB )
## Not sure why, but these give invalid operation :(
##if glValidateProgramARB and OpenGL.ERROR_CHECKING:
##	glValidateProgramARB.errcheck = _afterCheck( GL_OBJECT_VALIDATE_STATUS_ARB )

@lazy( glGetInfoLogARB )
def glGetInfoLogARB( baseOperation, obj ):
    """Retrieve the program/shader's error messages as a Python string

    returns string which is '' if no message
    """
    length = int(glGetObjectParameterivARB(obj, GL_INFO_LOG_LENGTH_ARB))
    if length > 0:
        log = ctypes.create_string_buffer(length)
        baseOperation(obj, length, None, log)
        return log.value.strip(_NULL_8_BYTE) # null-termination
    return ''

@lazy( glGetAttachedObjectsARB )
def glGetAttachedObjectsARB( baseOperation, obj ):
    """Retrieve the attached objects as an array of GLhandleARB instances"""
    length= glGetObjectParameterivARB( obj, GL_OBJECT_ATTACHED_OBJECTS_ARB )
    if length > 0:
        storage = arrays.GLuintArray.zeros( (length,))
        baseOperation( obj, length, None, storage )
        return storage
    return arrays.GLuintArray.zeros( (0,))

@lazy( glGetShaderSourceARB )
def glGetShaderSourceARB( baseOperation, obj ):
    """Retrieve the program/shader's source code as a Python string

    returns string which is '' if no source code
    """
    length = int(glGetObjectParameterivARB(obj, GL_OBJECT_SHADER_SOURCE_LENGTH_ARB))
    if length > 0:
        source = ctypes.create_string_buffer(length)
        baseOperation(obj, length, None, source)
        return source.value.strip(_NULL_8_BYTE) # null-termination
    return ''

@lazy( glGetActiveUniformARB )
def glGetActiveUniformARB(baseOperation, program, index):
    """Retrieve the name, size and type of the uniform of the index in the program"""
    max_index = int(glGetObjectParameterivARB( program, GL_OBJECT_ACTIVE_UNIFORMS_ARB ))
    length = int(glGetObjectParameterivARB( program, GL_OBJECT_ACTIVE_UNIFORM_MAX_LENGTH_ARB))
    if index < max_index and index >= 0:
        if length > 0:
            name = ctypes.create_string_buffer(length)
            namelen = arrays.GLsizeiArray.zeros( (1,))
            size = arrays.GLintArray.zeros( (1,))
            gl_type = arrays.GLenumArray.zeros( (1,))
            baseOperation(program, index, length,namelen,size, gl_type, name)
            return name.value[:int(namelen[0])], size[0], gl_type[0]
        raise ValueError( """No currently specified uniform names""" )
    raise IndexError('Index %s out of range 0 to %i' % (index, max_index - 1, ))

@lazy( glGetUniformLocationARB )
def glGetUniformLocationARB( baseOperation, program, name ):
    """Check that name is a string with a null byte at the end of it"""
    if not name:
        raise ValueError( """Non-null name required""" )
    elif name[-1] != _NULL_8_BYTE:
        name = name + _NULL_8_BYTE
    return baseOperation( program, name )
