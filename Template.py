# -*- encoding: utf-8 -*-

import decimal_precision as dp
import time
import base64
from tempfile import TemporaryFile
import math
from osv import fields, osv
import tools
import ir
import pooler
import tools
from tools.translate import _
import csv
import sys
import os
import re

def _ListaTipiFile(self, cr, uid, context={}):
    return [("T", "Tutti i Modelli"), ('C', 'Per Categoria '), ('M', 'Per Modello')]



class product_template(osv.osv):

    _inherit = 'product.template'
    
    
    def _import_var(self, cr, uid, lines, tipo, context):
       # import pdb;pdb.set_trace()
        import_data = {'tipo_file':  tipo}
        inseriti = 0
        aggiornati = 0
        PrimaRiga = True
        for riga in  lines:
            #riga = riga.replace('"', '')
            #riga = riga.split(";")
            if PrimaRiga:
                testata = riga
                PrimaRiga = False
            else:
                if import_data['tipo_file'] == 'T':
                    #import pdb;pdb.set_trace()
                    #print riga
                    # il file deve aggiungere o aggiornare su tutti i template le relative tabelle varianti
                    TemplateIds = self.pool.get('product.template').search(cr, uid, [])
                    if TemplateIds:
                     for Template in TemplateIds:
                        # cerca l'esistenza della dimensione 
                        #import pdb;pdb.set_trace()
                        idDimensione = self.Check_Dimension(cr, uid, Template, riga, context)
                        param = [('name', '=', riga[2]), ('product_tmpl_id', "=", Template), ('dimension_id', '=', idDimensione[0])]
                        idDimensionValore = self.pool.get("product.variant.dimension.value").search(cr, uid, param)
                        if not idDimensionValore:
                            # non trovato inserisco
                            valore = {
                                      'name':riga[2],
                                      'desc_value':riga[3],
                                      'flag_obbl':riga[4],
                                      'product_tmpl_id':Template,
                                      'dimension_id':idDimensione[0],
                                      'price_extra':riga[5].replace(',', '.'),
                                      }
                            #import pdb;pdb.set_trace()
                            idDimensionValore = self.pool.get("product.variant.dimension.value").create(cr, uid, valore)
                            inseriti = +1
                        else:                            
                            #aggiorno il prezzo
                            valore = {
                                      'price_extra':riga[5].replace(',', '.'),
                                      }
                            #import pdb;pdb.set_trace()
                            ok = self.pool.get("product.variant.dimension.value").write(cr, uid, idDimensionValore, valore)
                            aggiornati = +1
                        
                
                if import_data['tipo_file'] == 'C':
                    for colonna in range(5, len(riga)):
                        #cicla su tutte le colonne che ci sono nel csv
                        #import pdb;pdb.set_trace()
                        param = [('name', 'ilike', testata[colonna] + "%")]
                        category_id = self.pool.get('product.category').search(cr, uid, param)
                        if category_id:
                           param = [('categ_id', "=", category_id[0])]
                           TemplateIds = self.pool.get('product.template').search(cr, uid, param)
                           if TemplateIds:
                               # presi tutti i template che appartengono alla categoria
                               for Template in TemplateIds:
                                    idDimensione = self.Check_Dimension(cr, uid, Template, riga, context)
                                    param = [('name', '=', riga[2]), ('product_tmpl_id', "=", Template), ('dimension_id', '=', idDimensione[0])]
                                    idDimensionValore = self.pool.get("product.variant.dimension.value").search(cr, uid, param)
                                    if not idDimensionValore:
                                        # non trovato inserisco
                                        valore = {
                                                  'name':riga[2],
                                                  'desc_value':riga[3],
                                                  'flag_obbl':riga[4],
                                                  'product_tmpl_id':Template,
                                                  'dimension_id':idDimensione[0],
                                                  'price_extra':riga[colonna].replace(',', '.'),
                                      }
                                        idDimensionValore = self.pool.get("product.variant.dimension.value").create(cr, uid, valore)
                                        inseriti = +1
                                    else:                            
                                        #aggiorno il prezzo
                                        valore = {
                                                  'price_extra':riga[colonna].replace(',', '.'),
                                                  }
                                        ok = self.pool.get("product.variant.dimension.value").write(cr, uid, idDimensionValore, valore)
                                        inseriti = +1
                if import_data['tipo_file'] == 'M':
                    #import pdb;pdb.set_trace()
                    for colonna in range(5, len(riga)):
                        #cicla su tutte le colonne che ci sono nel csv
                           param = [('codice_template', "=", testata[colonna])]
                           TemplateIds = self.pool.get('product.template').search(cr, uid, param)
                           if TemplateIds:
                               #trovato il template che ci interessa
                                    Template = TemplateIds[0]
                                    idDimensione = self.Check_Dimension(cr, uid, Template, riga, context)
                                    param = [('name', '=', riga[2]), ('product_tmpl_id', "=", Template), ('dimension_id', '=', idDimensione[0])]
                                    idDimensionValore = self.pool.get("product.variant.dimension.value").search(cr, uid, param)
                                    if not idDimensionValore:
                                        # non trovato inserisco
                                        valore = {
                                                  'name':riga[2],
                                                  'desc_value':riga[3],
                                                  'flag_obbl':riga[4],
                                                  'product_tmpl_id':Template,
                                                  'dimension_id':idDimensione[0],
                                                  'price_extra':riga[colonna].replace(',', '.'),
                                      }
                                        idDimensionValore = self.pool.get("product.variant.dimension.value").create(cr, uid, valore)
                                        aggiornati = +1
                                    else:                            
                                        #aggiorno il prezzo
                                        valore = {
                                                  'price_extra':riga[colonna].replace(',', '.'),
                                                  }
                                        ok = self.pool.get("product.variant.dimension.value").write(cr, uid, idDimensionValore, valore)
                                        aggiornati = +1
                             
                        
        return [inseriti, aggiornati]

    def Check_Dimension(self, cr, uid, Template, riga, context):
            #import pdb;pdb.set_trace()
            param = [('name', '=', riga[0]), ('product_tmpl_id', "=", Template)]
            idDimension = self.pool.get("product.variant.dimension.type").search(cr, uid, param)
            if not idDimension:
                    # non Trovato inserisce una nuova dimensione nel template
                            Dimensione = {
                                          'name':riga[0],
                                          'desc_type':riga[5],
                                          'flag_obbl':riga[4],
                                          'sequence':riga[1],
                                          'product_tmpl_id':Template,
                                          'allow_custom_value':True,
                                          }
                            idDimension = self.pool.get("product.variant.dimension.type").create(cr, uid, Dimensione)
                            idDimension = [idDimension]
            else:
                            Dimensione = {
                                          'name':riga[0],
                                          'sequence':riga[1],
                                          'desc_type':riga[5],
                                          'flag_obbl':riga[4],
                                          'product_tmpl_id':Template,
                                          'allow_custom_value':True,
                                          }
                            ok = self.pool.get("product.variant.dimension.type").write(cr, uid, idDimension, Dimensione)
                            
                
            return idDimension

    
    
    def run_auto_import_variant(self, cr, uid, automatic=False, use_new_cursor=False, context=None):
      pool = pooler.get_pool(cr.dbname)  
      #import pdb;pdb.set_trace()
      testo_log = """Inizio procedura di Aggiornamento/Inserimento Varianti Template """ + time.ctime() + '\n'
      percorso = '/home/openerp/filecsv'
      partner_obj = pool.get('product.template')
      if use_new_cursor:
        cr = pooler.get_db(use_new_cursor).cursor()
      elenco_csv = os.listdir(percorso)
      for filecsv in elenco_csv:
        codfor = filecsv.split(".")
        testo_log = testo_log + " analizzo file " + codfor[0] + ".csv \n"
        lines = csv.reader(open(percorso + '/' + filecsv, 'rb'), delimiter=";")
        if codfor[0].lower() == "variantitutti":
            #lancia il metodo per tutti i modelli
            #import pdb;pdb.set_trace() 
            res = self._import_var(cr, uid, lines, 'T', context)
        if codfor[0].lower() == "varianticat":
            #lancia il metodo per le categorie indicate
            #import pdb;pdb.set_trace() 
            res = self._import_var(cr, uid, lines, 'C', context)
        if codfor[0].lower() == "variantimod":
            #lancia il metodo per i modelli indicati
            #import pdb;pdb.set_trace() 
            res = self._import_var(cr, uid, lines, 'M', context)
        if res:  
          testo_log = testo_log + " Inseriti " + str(res[0]) + " Aggiornati " + str(res[1]) + " Varianti \n"
        else:
          testo_log = testo_log + " File non riconosciuto  " + codfor[0] + " non trovato  \n"
        os.remove(percorso + '/' + filecsv)
      testo_log = testo_log + " Operazione Teminata  alle " + time.ctime() + "\n"
      #invia e-mail
      type_ = 'plain'
      tools.email_send('OpenErp@mainettiomaf.it',
                       ['Giuseppe.Sciacco@mainetti.com'],
                       'Import Automatico Varianti Articoli',
                       testo_log,
                       subtype=type_,
                       )

        
      return
product_template()
