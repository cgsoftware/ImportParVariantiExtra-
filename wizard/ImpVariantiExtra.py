# -*- encoding: utf-8 -*-

import wizard
import decimal_precision as dp
import pooler
import time
from tools.translate import _
from osv import osv, fields
from tools.translate import _
import tools
import base64
from tempfile import TemporaryFile
from osv import osv, fields


def _ListaTipiFile(self, cr, uid, context={}):
    return [("T", "Tutti i Modelli"), ('C', 'Per Categoria '), ('M', 'Per Modello')]



class importa_varianti_template(osv.osv_memory):
    _name = 'importa.varianti.template'
    _description = 'Importa Varianti e prezzi extra da file csv '
    _columns = {
                'data': fields.binary('File', required=True),
                'tipo_file':fields.selection(_ListaTipiFile, 'Tipo Importazione', required=True),
         }
    
    def import_var(self, cr, uid, ids, context):
        
        import_data = self.browse(cr, uid, ids)[0]
        fileobj = TemporaryFile('w+')
        fileobj.write(base64.decodestring(import_data.data))
        fileobj.seek(0)
        PrimaRiga = True
        for riga in  fileobj.readlines():
            riga = riga.replace('"', '')
            riga = riga.split(";")
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
                                      'product_tmpl_id':Template,
                                      'dimension_id':idDimensione[0],
                                      'price_extra':riga[3].replace(',', '.'),
                                      }
                            #import pdb;pdb.set_trace()
                            idDimensionValore = self.pool.get("product.variant.dimension.value").create(cr, uid, valore)
                        else:                            
                            #aggiorno il prezzo
                            valore = {
                                      'price_extra':riga[3].replace(',', '.'),
                                      }
                            #import pdb;pdb.set_trace()
                            ok = self.pool.get("product.variant.dimension.value").write(cr, uid, idDimensionValore, valore)
                        
                
                if import_data['tipo_file'] == 'C':
                    for colonna in range(3, len(riga) + 1):
                        #cicla su tutte le colonne che ci sono nel csv
                        param = [('name', 'ilike', testata[colonna] + "%")]
                        category_id = self.pool.get('product.category'), search(cr, uid, param)
                        if category_id:
                           param = ['categ_id', "=", category_id[0]]
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
                                                  'product_tmpl_id':Template,
                                                  'dimension_id':idDimensione[0],
                                                  'price_extra':riga[colonna].replace(',', '.'),
                                      }
                                        idDimensionValore = self.pool.get("product.variant.dimension.value").create(cr, uid, valore)
                        else:                            
                            #aggiorno il prezzo
                            valore = {
                                      'price_extra':riga[colonna].replace(',', '.'),
                                      }
                            ok = self.pool.get("product.variant.dimension.value").write(cr, uid, idDimensionValore, valore)
                if import_data['tipo_file'] == 'M':
                    for colonna in range(3, len(riga) + 1):
                        #cicla su tutte le colonne che ci sono nel csv
                           param = ['codice', "=", testata[colonna]]
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
                                                  'product_tmpl_id':Template,
                                                  'dimension_id':idDimensione[0],
                                                  'price_extra':riga[colonna].replace(',', '.'),
                                      }
                                        idDimensionValore = self.pool.get("product.variant.dimension.value").create(cr, uid, valore)
                                    else:                            
                                        #aggiorno il prezzo
                                        valore = {
                                                  'price_extra':riga[colonna].replace(',', '.'),
                                                  }
                                        ok = self.pool.get("product.variant.dimension.value").write(cr, uid, idDimensionValore, valore)
                               
                        
        import pdb;pdb.set_trace()            
        fileobj.close()    
        return {}

    def Check_Dimension(self, cr, uid, Template, riga, context):
            param = [('name', '=', riga[0]), ('product_tmpl_id', "=", Template)]
            idDimension = self.pool.get("product.variant.dimension.type").search(cr, uid, param)
            if not idDimension:
                    # non Trovato inserisce una nuova dimensione nel template
                            Dimensione = {
                                          'name':riga[0],
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
                                          'product_tmpl_id':Template,
                                          'allow_custom_value':True,
                                          }
                            ok = self.pool.get("product.variant.dimension.type").write(cr, uid, idDimension, Dimensione)
                            
                
            return idDimension

  
  

importa_varianti_template()
