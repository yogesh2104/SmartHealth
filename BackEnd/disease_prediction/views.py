from rest_framework.views import APIView
from rest_framework.response import Response
from joblib import load
import pandas as pd
import numpy as np
import csv
from django.conf import settings



request_example={ 
  "abdominal cramp": "abdominal cramp",
  "abdominal distention":"abdominal distention",   
  "abnormal behavior":"abnormal behavior",
  "abnormal bleeding":"abnormal bleeding",
  "abnormal sensation":"abnormal sensation",
  "mental ability":"mental ability",
  "acquiring drinking alcohol taking lot time":"acquiring drinking alcohol taking lot time",
  
  "current_disease":"Abscess"
}

symptom_name = ['abdominal cramp', 'abdominal distention', 'abnormal behavior', 'abnormal bleeding', 'abnormal sensation', 'abnormally frequent', 'abscess', 'aching', 'acne', 'acquiring drinking alcohol taking lot time', 'affected part turning white', 'anemia', 'anxiety', 'arm', 'attack pain', 'back', 'bacterial infection', 'bad breath', 'bad smelling thin vaginal discharge', 'bad smelling vaginal discharge', 'barky cough', 'belching', 'better sitting worse lying', 'birth baby younger week gestational age', 'bleeding gum', 'bleeding skin', 'blindness', 'blindness one eye', 'blister sunlight', 'bloating', 'blood stool', 'blood urine', 'bloody diarrhea', 'blue', 'bluish skin coloration', 'blurred vision', 'blurry vision', 'body tremor', 'bone pain', 'bowed leg', 'breakdown skeletal muscle', 'breathing problem', 'bruising', 'burning', 'burning redness eye', 'burning stabbing pain', 'burning urination', 'certain thought repeatedly', 'change bowel movement', 'change breast shape', 'change color', 'change hair', 'change reflex', 'change skin color red black', 'change sleeping eating pattern', 'change taste', 'change voice', 'characteristic facial feature', 'characteristic rash', 'chest discomfort', 'chest pain', 'chest tightness', 'chill', 'chronic cough', 'chronic pain bladder', 'clenched fist overlapping finger', 'close object appear blurry', 'clumsy', 'cm lump skin', 'cold sweat', 'coma', 'confused thinking', 'confusion', 'constipation', 'coolness', 'coordination', 'cough bloody mucus', 'cough sputum production', 'coughing', 'coughing blood', 'coughing including coughing blood', 'coughing mucus', 'crawl', 'cry episode', 'dark urine', 'darker', 'daytime sleepiness', 'death child le one year age', 'decreased ability feel pain', 'decreased ability see', 'decreased ability think', 'decreased ability think remember', 'decreased ability turn', 'decreased appetite', 'decreased motivation', 'decreased range motion', 'decreased taste', 'decreased vision', 'dehydration', 'delayed physical growth', 'delirium', 'delusion', 'dementia', 'depending subtype abdominal pain', 'depends organ involved', 'depressed mood', 'depression', 'dermatitis herpetiformis', 'developmental disability', 'diarrhea', 'diarrhea may bloody', 'diarrhea mixed blood', 'diarrhoea', 'difficulty breathing', 'difficulty cutting', 'difficulty eating', 'difficulty getting pregnant', 'difficulty remembering recent event', 'difficulty swallowing', 'difficulty walking', 'dimpling skin', 'discharge penis', 'disorientation', 'distant object appear blurry', 'distorted blurred vision distance', 'dizziness', 'double vision', 'drinking large amount alcohol long period', 'drooping eyelid', 'dry cough', 'dry damp skin', 'dry eye', 'dry mouth', 'ear pain', 'easy prolonged bleeding', 'emotional problem', 'enlarged lymph node neck', 'enlarged spleen', 'enlarged thyroid', 'enlargement thyroid', 'enlargement tonsil', 'episode severe', 'erythema marginatum', 'excess hair', 'excessive amount uterine bleeding', 'excessive daytime sleepiness', 'excessive salivation', 'expanding area redness site tick bite', 'extreme sadness', 'extremity weakness', 'eye pain', 'eye strain', 'eyestrain', 'fast heart rate', 'fast heartbeat', 'fatigue', 'fear water', 'feel need check thing repeatedly', 'feeling cold', 'feeling faint upon standing', 'feeling generally unwell', 'feeling like passing', 'feeling need urinate right away', 'feeling tired', 'feeling tired time', 'fever', 'firm', 'flat discolored spot bump may blister', 'flu like illness', 'flu like symptom', 'fluid filled blister scab', 'fluid nipple', 'frequent infection', 'frequent urination', 'fullness', 'gas', 'gradual loss coordination', 'growth delay', 'gum disease', 'hair loss', 'half ring finger', 'hallucination', 'hallucination usually hearing voice', 'hard swelling skin', 'hard time reading small print', 'headache', 'hearing loss', 'hearing sound external sound present', 'heartburn', 'heat intolerance', 'heavy period', 'high blood pressure', 'high body temperature', 'hoarse voice', 'hold reading material farther away', 'impaired communication', 'inability child', 'inability move facial muscle one side', 'inability move feel one side body', 'increased breath rate', 'increased breathing rate', 'increased fat', 'increased heart rate', 'increased hunger', 'increased risk broken bone', 'increased risk infection', 'increased thirst', 'increasing weakening', 'index', 'infertility', 'inflamed eye', 'insomnia', 'intellectual disability', 'involuntary muscle movement', 'involuntary sleep episode', 'irregular edge', 'irregular menstrual period', 'irregular menstruation', 'irritability', 'irritation', 'itchiness', 'itching', 'itching genital area', 'itching result trouble sleeping', 'itchy', 'itchy blister', 'itchy bump', 'itchy ear', 'jaundice', 'jaw', 'jerky body movement', 'joint bone pain', 'joint swelling', 'large amount watery diarrhea', 'large forehead', 'large lymph node', 'large lymph node around neck', 'leg swelling', 'light sensitivity', 'little pain', 'localized breast pain redness', 'long term fatigue', 'loose frequent bowel movement', 'loose teeth', 'loss appetite', 'loss consciousness may sweating', 'loss hair part head body', 'loss lot blood childbirth', 'loss smell', 'loss vision one side', 'low blood pressure', 'low energy', 'low red blood cell', 'lower abdominal pain', 'lump breast', 'lump bump neck', 'maculopapular rash', 'malabsorption', 'may symptom', 'memory problem', 'mental ability', 'mental change', 'mid dilated pupil', 'middle finger', 'mild moderate intellectual disability', 'minimal', 'missed period', 'mole increasing size', 'mood change', 'mood swing', 'mouth sore', 'mouth ulcer', 'multiple painful joint', 'muscle ache difficulty breathing', 'muscle cramp', 'muscle joint pain', 'muscle spasm', 'muscle weakness', 'muscle weakness beginning foot hand', 'muscle weakness resulting inability move', 'muscular pain', 'myalgia', 'nausea', 'nausea vomiting', 'nausea vomiting weight loss dehydration occur', 'nearly undetectable spell', 'nearsightedness', 'neck', 'neck stiffness', 'needing urinate often', 'newly inverted nipple', 'non itchy skin ulcer', 'non painful cyst middle eyelid', 'nonaligned eye', 'none non specific', 'numbness', 'object different size eye', 'one eye myopia eye hyperopia', 'opening upper lip may extend nose palate', 'others', 'overlying redness', 'pain along inside edge shinbone', 'pain area', 'pain around ear', 'pain doesnt go shingle', 'pain going leg lower back', 'pain sex', 'pain specific bone', 'painful', 'painful blister lower leg', 'painful heavy period', 'painful joint base big toe', 'painful rash occurring stripe', 'painful skin', 'painful swelling parotid gland', 'painful swollen joint', 'painful tender outer part elbow', 'painless', 'painless lump', 'pale color', 'pale skin', 'pallor', 'paralysis', 'patch thick', 'patch white skin', 'perform certain routine repeatedly', 'period vigorous shaking', 'persistent rough white red patch mouth lasting longer week', 'photophobia', 'physical disability', 'pimple like rash', 'pinkish', 'playing video game extremely long period time', 'poor ability tolerate cold', 'poor appetite', 'poor coordination', 'poor tolerance heat', 'post nasal drip', 'problem language', 'problem mood', 'problem understanding speaking', 'problem vision', 'profuse sweating', 'progressive muscle weakness', 'prolonged', 'prolonged cough', 'prominent', 'protein urine', 'psychosis', 'pulsing pain', 'purple colored skin affected area', 'purple colored skin lesion', 'raised', 'raised red blue lesion', 'random outburst laughter', 'rapid breathing', 'recurring episode wheezing', 'red', 'red eye', 'red purple darker skin', 'red rash', 'red scaly patch skin breast', 'red skin', 'red spot white eye', 'red without blister', 'reddish eye', 'redness', 'redness eye', 'repetitive behavior', 'restricted interest', 'right lower abdominal pain', 'rigidity', 'ringing ear heartbeat', 'rough skin growth', 'runny nose', 'scaly patch skin', 'scratchiness', 'seizure', 'sensitivity smell', 'sensitivity sound', 'severe intellectual disability', 'severe pain', 'severe pain lower back abdomen', 'shakiness', 'shaking', 'sharp chest pain', 'shivering', 'shock like pain one side face last second minute', 'short height', 'short stature', 'shortness breath', 'sit', 'skin blister', 'skin breakdown', 'skin lesion generally pink color project outward', 'skin peeling', 'sleep problem', 'sleeping problem', 'slowness movement', 'small', 'small blister break open form painful ulcer', 'small blister surrounding swelling', 'small face', 'small head', 'small jaw', 'sneezing', 'social withdrawal', 'sometimes symptom', 'sore arm leg', 'sore throat', 'sore wrist', 'stiff muscle', 'stiff neck', 'stiffness', 'stomach pain', 'stroke', 'stuffy itchy nose', 'stunted growth', 'sudden', 'sudden loss muscle strength', 'sweat', 'swell pain near tumor', 'swelling', 'swelling abdomen', 'swelling around eye', 'swelling hand foot', 'swollen', 'swollen hand foot', 'swollen lymph node', 'taste acid', 'temporary fleeting vision one eye', 'tender breast', 'testicular pain', 'tingling', 'tingling hand foot', 'tingling thumb', 'tiredness', 'tooth loss', 'tremor', 'triangular tissue growth cornea', 'trouble breathing nose', 'trouble coordination', 'trouble opening mouth', 'trouble seeing', 'trouble sensation', 'trouble sleeping', 'trouble social interaction', 'trouble speaking', 'trouble swallowing', 'trouble talking', 'trouble walking', 'typically none', 'ulcer', 'ulcer around genitals', 'ulceration', 'unable move', 'unexplained weight loss', 'unintended weight loss', 'unpleasant smell present breath', 'upper abdominal pain', 'usage resulting problem', 'vaginal bleeding', 'vaginal bleeding without pain', 'vaginal discharge', 'variable', 'vary depending part brain involved', 'varying degree muscle weakness', 'velvety skin', 'vision loss', 'vomiting', 'warm', 'wart', 'watery eye', 'weak grip', 'weak muscle', 'weakness limb', 'weakness numbness affected leg', 'webbed neck', 'weight gain', 'wet', 'wheezing', 'white patch vaginal discharge', 'widespread pain', 'withdrawal occurring stopping', 'worrying', 'yellow skin', 'yellowish coloration skin white eye', 'yellowish skin', 'yellowish skin crust']





class DiseasePredictionView(APIView):
    
    def get_row_by_disease(csv_file, disease_name):
        with open(csv_file, 'r', encoding='utf-8', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['disease'] == disease_name:
                    return row
        return []
    

    def post(self, request):

        print("Entering DiseasePredictionView...")
        symptoms=request.data
        # print(f"body: {symptoms}")

        if len(symptoms) == 0:
            return Response(None) 
        
        current_disease_symptom = []
        if 'current_disease' in symptoms:
            current_disease = symptoms.get('current_disease')
            current_disease_symptom = DiseasePredictionView.get_row_by_disease('./dataset/test_data.csv', current_disease)


        arr1 = []
        for symptom in symptom_name:
            if symptom in symptoms or symptom in current_disease_symptom:
                arr1.append(1)
            elif "current_disease" in symptoms:
                arr1.append(1)
            else:
                arr1.append(0)    
            
               
        # Prepare Test Data
        df_test = pd.DataFrame(columns=list(symptom_name))
        df_test.loc[0] = arr1
        # print(df_test)

        # Load pre-trained model
        clf = load(str("./saved_model/decision_tree.joblib"))

        # Predict Disease
        result = None
        try:
            result = clf.predict(df_test)
        except:
            print('Exception occured')
       
        return Response(result)
        

