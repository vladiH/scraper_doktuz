import os
import pandas as pd
from datetime import datetime
from config import Config, Logger
from src.infrastruture.external.mysql import MysqlConnection
from src.infrastruture.external.postgresql import PostgresConnection
from src.infrastruture.repositories.doktuz_imp import DoktuzRepositoryImp
class SaveExcelPipeline:

    def __init__(self,host, data_base, user, password, port):
        self.host = host
        self.data_base = data_base
        self.user = user
        self.password = password
        self.port = port
        self.columns = [
                        'dni',
                        'ape_nombres',
                        'edad',
                        'proyecto',
                        'area',
                        'empresa',
                        'tlf_contacto',
                        'correo',
                        'tipo_atencion',
                        'tipo_examen',
                        'fecha_atencion',
                        'sexo',
                        'procedencia',
                        'estado_civil',
                        'prof_ocup',
                        'antecedentes_personales',
                        'antecedentes_familiares',
                        'ram',
                        'habitos_frec_alcohol',
                        'habitos_nro_cig_x_dia',
                        'habitos_drogas',
                        'habitos_medicamentos',
                        'antecedentes_ocupacionales',
                        'accidentes_trabajo',
                        'trabajo_actual',
                        'riesgos_ocupacionales',
                        'proteccion_personal',
                        'anamnesis',
                        'pa',
                        'dx_pa',
                        'fc',
                        'fr',
                        'peso',
                        'talla',
                        'imc',
                        'p_abdominal',
                        'diagnostico_nutricional',
                        'examen_fisico',
                        'sistema_muculo_esqueletico_examens',
                        'sistema_muculo_esqueletico_diagnostico_1',
                        'sistema_muculo_esqueletico_diagnostico_2',
                        'sistema_muculo_esqueletico_diagnostico_3',
                        'hemograma',
                        'leucocitos',
                        'hemoglobina',
                        'hematocrito',
                        'hematíes',
                        'segmentados',
                        'eosinófilos',
                        'linfocitos',
                        'vcm',
                        'hcm',
                        'rcto_plaquetas',
                        'tifico_o',
                        'tifico_h',
                        'paratifico_a',
                        'glucosa',
                        'colesterol',
                        'trigliceridos',
                        'brucella',
                        'examen_orina',
                        'tgo',
                        'tgp',
                        'urea',
                        'creatinina',
                        'grupo_sanguineo',
                        'factor_rh',
                        'bk_esputo_muestra_1',
                        'bk_esputo_muestra_2',
                        'bk_esputo_muestra_3',
                        'parasitologico_muestra_1',
                        'parasitologico_muestra_2',
                        'parasitologico_muestra_3',
                        'hepatitis_igm',
                        'hdl',
                        'ldl',
                        'vldl',
                        'cocaina',
                        'marihuana',
                        'plomo_sangre',
                        'oftalmologia_diagnostico_1',
                        'oftalmologia_diagnostico_2',
                        'oftalmologia_diagnostico_3',
                        'oftalmologia_diagnostico_4',
                        'oftalmologia_diagnostico_5',
                        'oftalmologia_agudeza_visual_lejos_sin_correctores_od',
                        'oftalmologia_agudeza_visual_lejos_sin_correctores_oi',
                        'oftalmologia_agudeza_visual_lejos_con_correctores_od',
                        'oftalmologia_agudeza_visual_lejos_con_correctores_id',
                        'oftalmologia_agudeza_visual_cerca_sin_correctores_od',
                        'oftalmologia_agudeza_visual_cerca_sin_correctores_oi',
                        'oftalmologia_agudeza_visual_cerca_con_correctores_od',
                        'oftalmologia_agudeza_visual_cerca_con_correctores_id',
                        'oftalmologia_vision_colores_oi',
                        'oftalmologia_vision_colores_od',
                        'oftalmologia_vision_profundidad',
                        'audiometria_diagnostico_oido_derecho',
                        'audiometria_diagnostico_oido_izquierdo',
                        'audiometria_via_aerea_oido_derecho_250',
                        'audiometria_via_aerea_oido_derecho_500',
                        'audiometria_via_aerea_oido_derecho_1000',
                        'audiometria_via_aerea_oido_derecho_2000',
                        'audiometria_via_aerea_oido_derecho_3000',
                        'audiometria_via_aerea_oido_derecho_4000',
                        'audiometria_via_aerea_oido_derecho_6000',
                        'audiometria_via_aerea_oido_derecho_8000',
                        'audiometria_via_aerea_oido_izquierdo_250',
                        'audiometria_via_aerea_oido_izquierdo_500',
                        'audiometria_via_aerea_oido_izquierdo_1000',
                        'audiometria_via_aerea_oido_izquierdo_2000',
                        'audiometria_via_aerea_oido_izquierdo_3000',
                        'audiometria_via_aerea_oido_izquierdo_4000',
                        'audiometria_via_aerea_oido_izquierdo_6000',
                        'audiometria_via_aerea_oido_izquierdo_8000',
                        'audiometria_via_osea_oido_derecho_250',
                        'audiometria_via_osea_oido_derecho_500',
                        'audiometria_via_osea_oido_derecho_1000',
                        'audiometria_via_osea_oido_derecho_2000',
                        'audiometria_via_osea_oido_derecho_3000',
                        'audiometria_via_osea_oido_derecho_4000',
                        'audiometria_via_osea_oido_derecho_6000',
                        'audiometria_via_osea_oido_derecho_8000',
                        'audiometria_via_osea_oido_izquerdo_250',
                        'audiometria_via_osea_oido_izquerdo_500',
                        'audiometria_via_osea_oido_izquerdo_1000',
                        'audiometria_via_osea_oido_izquerdo_2000',
                        'audiometria_via_osea_oido_izquerdo_3000',
                        'audiometria_via_osea_oido_izquerdo_4000',
                        'audiometria_via_osea_oido_izquerdo_6000',
                        'audiometria_via_osea_oido_izquerdo_8000',
                        'otoscopia_oido_derecho',
                        'otoscopia_oido_izquierdo',
                        'otoscopia_obs_otoscopia_od',
                        'otoscopia_obs_otoscopia_oi',
                        'antecedentes_otologicos_tiempo_diario_exposicion_horas',
                        'antecedentes_otologicos_anos_exposicion',
                        'antecedentes_otologicos_protectores_auditivos',
                        'espirometia_calidad',
                        'espirometia_diagnostico',
                        'electrocardiograma_diagnostico',
                        'rayos_x_torax_diagnostico',
                        'rayo_x_lumbar_diagnostico',
                        'examen_dematologico_diagnostico_1',
                        'examen_dematologico_diagnostico_2',
                        'examen_dematologico_diagnostico_3',
                        'examen_neurologico_diagnostico_1',
                        'examen_neurologico_diagnostico_2',
                        'examen_neurologico_diagnostico_3',
                        'odontologia_diagnostico',
                        'psicologia_aptitud',
                        'psicologia_acrofobia',
                        'psicologia_claustrofobia',
                        'psicologia_fatiga',
                        'psicologia_recomendaciones',
                        'altura_fisica_aptitud',
                        'espacios_confinados_aptitud',
                        'laboratorio_diagnostico_1',
                        'laboratorio_diagnostico_2',
                        'laboratorio_diagnostico_3',
                        'laboratorio_diagnostico_4',
                        'laboratorio_diagnostico_5',
                        'hallazgos_diagnostico_1',
                        'hallazgos_cie_1_10',
                        'hallazgos_diagnostico_2',
                        'hallazgos_cie_2_10',
                        'hallazgos_diagnostico_3',
                        'hallazgos_cie_3_10',
                        'hallazgos_diagnostico_4',
                        'hallazgos_cie_4_10',
                        'hallazgos_diagnostico_5',
                        'hallazgos_cie_5_10',
                        'hallazgos_diagnostico_6',
                        'hallazgos_cie_6_10',
                        'hallazgos_diagnostico_7',
                        'hallazgos_cie_7_10',
                        'hallazgos_diagnostico_8',
                        'hallazgos_cie_8_10',
                        'hallazgos_diagnostico_9',
                        'hallazgos_cie_9_10',
                        'hallazgos_diagnostico_10',
                        'hallazgos_cie_10_10',
                        'hallazgos_diagnostico_11',
                        'hallazgos_cie_11_10',
                        'hallazgos_diagnostico_12',
                        'hallazgos_cie_12_10',
                        'hallazgos_diagnostico_13',
                        'hallazgos_cie_13_10',
                        'hallazgos_diagnostico_14',
                        'hallazgos_cie_14_10',
                        'hallazgos_diagnostico_15',
                        'hallazgos_cie_15_10',
                        'recomendaciones_1',
                        'recomendaciones_2',
                        'recomendaciones_3',
                        'recomendaciones_4',
                        'recomendaciones_5',
                        'recomendaciones_6',
                        'recomendaciones_7',
                        'recomendaciones_8',
                        'recomendaciones_9',
                        'recomendaciones_10',
                        'recomendaciones_11',
                        'recomendaciones_12',
                        'recomendaciones_13',
                        'recomendaciones_14',
                        'recomendaciones_15',
                        'enfermedad_ocupacional',
                        'enfermedad_comun',
                        'aptitud',
                        'restricciones',
                        'observaciones',
                        'fecha_reevaluaciones',
                        'control',
                        'levantamiento_restricciones',
                        'fecha_emision',
                        'psicosensometrico',
                        'prueba_esfuerzo'
        ]
    

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host = Config.HOST,
            data_base = Config.DATA_BASE,
            user = Config.USER,
            password = Config.PASSWORD,
            port = Config.PORT
        )
    def open_spider(self, spider):
        try:
            self.db = PostgresConnection(self.host, self.data_base, self.user, self.password, self.port)
            self.db.connect()
            Logger.info("SaveExcelPipeline: Connected to database")
            self.repository = DoktuzRepositoryImp(self.db)
        except Exception as e:
            Logger.critical('SaveExcelPipeline.open_spider: ', exc_info=True)
            raise e

    def close_spider(self, spider):
        self.db.close()

    def process_item(self, item, spider):
        try:
            for file in item['file_paths']:
                df = pd.read_excel(file)
                df = df.iloc[2:,:]
                df.reset_index()
                df.columns = self.columns
                df.insert(0, 'date_sys', datetime.now())
                #df.to_excel(os.path.basename(file))
                self.repository.save_excel_data(df)
                #df.to_sql('audit_data', self.engine, if_exists='append', index=False)
            
        except Exception as e:
            Logger.error('SaveExcelPipeline: fail when spider was processing data from excel: {} '.format(
                item
            ), exc_info=True)
            raise e