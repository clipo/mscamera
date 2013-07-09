use_osgeo = False
try:
  from osgeo import _gdal
  use_osgeo = True
except ImportError:
  import _gdal

def GetBlockSize(band):
  if (use_osgeo):
    return band.GetBlockSize()
  else:
    x = _gdal.ptrcreate('int', 0, 2)
    _gdal.GDALGetBlockSize(band._o, x, _gdal.ptradd(x, 1))
    result = (_gdal.ptrvalue(x, 0), _gdal.ptrvalue(x, 1))
    _gdal.ptrfree(x)
    return result
