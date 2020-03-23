# TODO BORRAR
# En este script se incluirán todas las funciones de utilidades utilizadas a lo largo del proyecto
# Es importante tener en cuenta y respetar que cualquier función dentro de la clase Helpers sea independiente del
# resto del proyecto (es decir, que pudiese copiarse y pegarse a otro proyecto sin generar errores y/o dependencias)
import platform
import struct

class Helpers:
	"""
	Utilities class.

	``Helpers`` class is not instantiable. Every function here is invoked referencing directly to the class.
	"""

	@staticmethod
	def get_os_architecture():
		"""
		Obtains the name of the Operative System and the architecture (32 or 64 bits) where the software is
		being executed in lower case.

		:return: Operative System and architecture values as tuple
		:rtype: (str, str)
		"""
		return platform.system().lower(), struct.calcsize('P') * 8
