import config
import infermedica_api

class mIntermedica(object):
    def __init__(self):
        config.setup()
        self.api = infermedica_api.get_api()
    def search(self, phrase, sex="male"):
        result = self.api.search(phrase, sex=sex)
        return result
    def getSymptoms(self):
        symptoms = self.api.symptoms_list()
        return symptoms
    def parseSearch(self, search):
        parsed = {}
        for item in search:
            parsed[item["label"]] = item["id"]
        return parsed, list(parsed.keys()), list(parsed.values())
    def diagnose(self, symptoms, sex="male", age="30"):
        request = infermedica_api.Diagnosis(sex=sex, age=age)
        for symptom in symptoms:
            request.add_symptom(symptom["id"], symptom["presence"])
        request = self.api.diagnosis(request)
        return request
    

if __name__ == "__main__":
    test = mIntermedica()
    phrase = test.search("headache")
    print(phrase)
    print(test.parseSearch(phrase))
    testD = [{'id': 's_1422', 'presence': 'present'}, {'id': 's_586', 'presence': 'absent'}, {'id': 's_547', 'presence': 'absent'}]
    #print(test.diagnose([dict(id="s_117", presence='present'), dict(id="s_118", presence='present')]))
    print(test.diagnose(testD))
