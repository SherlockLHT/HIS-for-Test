#coding:utf-8
import soaplib

from soaplib.core.server import wsgi
from soaplib.core.service import DefinitionBase
from soaplib.core.service import soap
from soaplib.core.model.clazz import Array
from soaplib.core.model.clazz import ClassModel
from soaplib.core.model.primitive import Integer,String
from PatientData import data

# 请求信息类
class TestRequestInfo(ClassModel):
    __namespace__ = "TestRequestInfo"
    reqNo           = String

# 返回信息类
class ResultInfo(ClassModel):
    __namespace__ = "ResultInfo"
    patient_id    = String
    patient_name  = String
    simple_id     = String
    patient_sex   = String
    patient_age   = String
    reagent       = String

# 请求方法
def exeRules(sample_id):
    result_info = ResultInfo()
    for patient_info in data:
        if sample_id == patient_info['sample_id']:
            result_info.patient_id = patient_info['Patient_id']
            result_info.patient_name = patient_info['Patient_name']
            result_info.simple_id = patient_info['sample_id']
            result_info.patient_sex = patient_info['sex']
            result_info.patient_age = patient_info['age']
            result_info.reagent = patient_info['reagent']
            break
    return result_info
        
class HISService(DefinitionBase):  #this is a web service
        @soap(String, _returns=ResultInfo)
        def GetPatientInfoBySampleID(self, sample_id):
            try:
                resInfo = exeRules(sample_id)
                return resInfo
            except Exception as e:
                print e
                raise e


if __name__=='__main__':
        try:
            print 'service start'
            from wsgiref.simple_server import make_server
            soap_application = soaplib.core.Application([HISService], 'tns')
            wsgi_application = wsgi.Application(soap_application)
            server = make_server('192.168.1.107', 1524, wsgi_application)
            server.serve_forever()
        except ImportError:
                print 'error'