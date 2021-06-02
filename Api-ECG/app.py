from flask import Flask,request,jsonify,Response
from flask_pymongo import  PyMongo
from bson import json_util
import json
import scipy.signal as signal
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import scipy.io as sio
import numpy as np
import pyrebase
import neurokit2 as nk
import matplotlib.pyplot as plt
import scipy.io as sio





config={
    "apiKey": "AIzaSyAFGQe3ifaAnf5ZnT4WkjwP8AjaC2-I8wc",
   "authDomain": "pacientespicture.firebaseapp.com",
  "databaseURL": "https://pacientespicture.firebaseio.com",
    "projectId": "pacientespicture",
   "storageBucket": "pacientespicture.appspot.com",
   "messagingSenderId": "948345356182",
  "appId": "1:948345356182:web:f942522f157fc46f4d67b7",
  "measurementId": "G-J3PR46H9RP"
}
firebase=pyrebase.initialize_app(config)
db=firebase.database()
# Para cargar imagenes
storage=firebase.storage()
# Inicializar Flask
app=Flask(__name__)
app.config['MONGO_URI']="mongodb+srv://stalyn_izack:Recreo.25@pacientesdb.7fhbe.mongodb.net/testDb?retryWrites=true&w=majority"
mongo=PyMongo(app)
mat=sio.loadmat('cu01m')
# Transformar de .mat a arreglos


def transform_funcions(signal):
   # z = np.append(signal, 0)

    # Tomamo los primeros segundos
    y= mat['val'][0][1:2500]
    return  y

# Funciones para graficar
def create_figure(signal,Fs):
    # Para preprocesar la señal
    ySana_2500=signal
    T = 1.0 / Fs
    longitud_senial = len(ySana_2500)
    tiempo_ySana = list(range(0, longitud_senial))
    tiempo_ySana = np.array(tiempo_ySana) / 250
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.plot(tiempo_ySana, ySana_2500)

    # Correccion de desplazamiento de línea de base
    # Normalizar los datos entre 0 y 1
    minYS = min(ySana_2500);
    maxYS = max(ySana_2500);
    ySanaNorm = (ySana_2500 - minYS) / (maxYS - minYS);
    x = np.linspace(0.0, longitud_senial * T, longitud_senial)
    return fig,x,Fs,signal,ySanaNorm

def segment(yClean):
    ECG_signal, info = nk.ecg_process(yClean, sampling_rate=1000)
    # Visualise the processing

    # plt.savefig('./images/signal_varios.png')

    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    nk.ecg_plot(ECG_signal, sampling_rate=1000)
    return nk.ecg_plot(ECG_signal, sampling_rate=1000)
    # plt.close()



def clean_signal(ySanaNorm,Fs,x):

    # Filtrado ButterWord,paso bajo
    b, a = signal.butter(4, 50 / (Fs / 2), 'low')
    # Compute filtered signal
    tempf = signal.filtfilt(b, a, ySanaNorm)
    nyq_rate = Fs / 2.0
    # The desired width of the transition from pass to stop.
    width = 5.0 / nyq_rate
    # The desired attenuation in the stop band, in dB.
    ripple_db = 60.0
    # Compute the order and Kaiser parameter for the FIR filter.
    O, beta = signal.kaiserord(ripple_db, width)
    # The cutoff frequency of the filter.
    cutoff_hz = 4.0
    taps = signal.firwin(O, cutoff_hz / nyq_rate, window=('kaiser', beta), pass_zero=False)
    # Use lfilter to filter x with the FIR filter.
    y_filt = signal.lfilter(taps, 1.0, tempf)
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.plot(x, y_filt, color='g', linewidth=0.7)

    return  fig,y_filt


# Serivicios Rest
@app.route('/listar',methods=['GET'])
def get_users():

    users=mongo.db.pacientes.find({},{'_id':0})
    response = json_util.dumps(users)
    print(users)
    return Response(response,mimetype='application/json')


@app.route('/listar/<id>',methods=['GET'])
def get_user(id):
    number=int(id)
    pacient= mongo.db.pacientes.find_one({"ci": number},{'_id':0})
    response=json_util.dumps(pacient)
    return  Response(response,mimetype='application/json')


@app.route('/eliminar/<id>',methods=['DELETE'])
def delete_user(id):
    number=int(id)
    mongo.db.pacientes.delete_one({"ci": number})
    return  'Registro con ci: '+id+'borrado'


@app.route('/users',methods=['PUT'])
def update_user():
    #Recibir data
    ci = request.json['ci']
    name = request.json['name']
    address = request.json['address']
    signal=request.json['signal']
    if ci and name and address and signal:
        mongo.db.pacientes.update_one({'ci':ci},{'$set':{
            'ci': ci,
            'name': name,
            'address': address,
            'signal':signal
        }})
        response=jsonify({'message':'User '+str(ci)+' se actualizaco correctamente'})
    return response


@app.route('/user',methods=['POST'])
def create_user():
    #Recibir data
    ci=request.json['ci']
    name=request.json['name']
    address = request.json['address']
    #signal = request.json['signal']
    #signal=mat
    signal_a=transform_funcions(mat)
    # load signal
    fig, x, Fs, signal, ySanaNorm = create_figure(signal_a,250)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    path_on_cloud = "images/"+str(ci)+"/signal.jpg"
    # preprocesing
    fig_2,y_filt=clean_signal(ySanaNorm,Fs,x)
    output_2 = io.BytesIO()
    FigureCanvas(fig_2).print_png(output_2)
    path_on_cloud_2 = "images-prep/" + str(ci) + "/signal.jpg"
    print(path_on_cloud)
    # Proceso
    fig_3=segment(y_filt)
    output_3 = io.BytesIO()
    FigureCanvas(fig_3).print_png(output_3)
    path_on_cloud_3 = "images-picos/" + str(ci) + "/signal.jpg"
    # para ingresar a firebase
    numpyData = signal_a.tolist()
    encodedNumpyData = json.dumps(numpyData)  # use dump() to write array into file
    path_local = output.getvalue()
    path_local_2=output_2.getvalue()
    path_local_3 = output_3.getvalue()
    # Load 1
    storage.child(path_on_cloud).put(path_local)
    imagen=storage.child(path_on_cloud).get_url(1)
    # Load 2
    storage.child(path_on_cloud_2).put(path_local_2)
    imagen_2 = storage.child(path_on_cloud_2).get_url(1)
    # Load 3
    storage.child(path_on_cloud_3).put(path_local_3)
    imagen_3 = storage.child(path_on_cloud_3).get_url(1)
    #print('este es URL',storage.child(path_on_cloud).get_url(1))
    if ci and name and address:
        data={
            'ci': ci,
            'name': name,
            'address': address,
            #'signal': json.dumps(numpyData),
            'signal':numpyData,
            'imagen':imagen,
            'clean':imagen_2,
            'segmento':imagen_3

        }
        # para set la primary key
        #db.child().child("ci").push(data)
        #db.child().push(data)
        id=mongo.db.pacientes.insert(
          data)
        #response={
         #  'id':str(id),
          #  'ci':ci,
           # 'name':name,
           # 'address':address,
            #'signal': encodedNumpyData
        #}
        return 'Ingreso'
            #Response(output.getvalue(), mimetype='image/png')


    else:
        {'message':'recevided'}

    return 'Ingreso'
        #Response(output.getvalue(), mimetype='image/png')



@app.errorhandler(404)
def not_found(error=None):
    message=jsonify({
        'message':'Resource Not Found'+request.url,
        'status':404
    })
    message.status_code=404
    return message


if __name__=="__main__":
    app.run(debug=True)


#app.run(host="0.0.0.0", port=5000, debug=True)