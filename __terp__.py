# -*- encoding: utf-8 -*-
##############################################################################
#    
#    Copyright (C) 2009 Italian Community (http://www). 
#    All Rights Reserved
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'IMPORT DA EXCEL DELLE TABELLE VARIANTI E TEMPLATE',
    'version': '0.1',
    'category': 'Localisation/Italy',
    'description': """Importazione Varianti Articoli ed exstra, formati csv/txt 
      esistono 3 tipo di importazione:
      1) valido per tutti i template
      2) valido per categoria 
      3) valido per template
      
      sulla prima riga del file excel vanno indicati i campi
      1) DIMENSION,SEQ,VALUE,EXTRA
      2) DIMENSION,SEQ,VALUE,ELENCO CATEGORIE
      3) DIMENSION,SEQ,VALUE,ELENCO MODELLI ARTICOLO
      """,
    'author': 'C & G Software sas',
    'website': 'http://www.cgsoftware.it',
    "depends" : ['product_variant_multi', 'product'],
    "update_xml" : ['wizard/ImpVariantiExtra.xml'],
    "active": False,
    "installable": True
}

