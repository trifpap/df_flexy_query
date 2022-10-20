import streamlit as st 
import pandas as pd

st.header('Flexible Data Filtering UI')

# set csv file
data = 'data/items_en_modified_181022_132918_rev.csv'

df = pd.read_csv(data, sep = ';')

st.subheader('Data table from items_en_modified_181022_132918_rev.csv')
st.write(df)

# count no. of lines
st.write("Number of lines present:-", 
      len(df))

df = df.sort_values(by='Parent',ascending=True)
parent_sort=df.Parent.unique()

with st.expander('Show UI Specification', expanded=False):
    with st.echo():
        UI_SPECIFICATION = [
            {   
                'selector': {
                    'key': 'selector_frgnname',
                    'type': st.checkbox,
                    'label': 'FrgnName - Ξένη Περιγρ. (required)',
                    'kwargs': {'value': True, 'disabled': True},
                },
                'input': {
                    'key': 'input_frgnname',
                    'type': st.text_input,
                    'dtype': str,
                    'label': 'FrgnName - Ξένη Περιγρ.',
                    'db_col': 'FrgnName',
                    'kwargs': {},
                },
            },
            {   
                'selector': {
                    'key': 'selector_supplcatnum',
                    'type': st.checkbox,
                    'label': 'SupplCatNum - Προμηθ.',
                    'kwargs': {'value': False},
                },
                'input': {
                    'key': 'input_supplcatnum',
                    'type': st.multiselect,
                    'dtype': list,
                    'label': 'SupplCatNum - Προμηθευτής',
                    'db_col': 'SupplCatNum',
                    'kwargs': {'options': df['SupplCatNum'].unique()},
                },
            },
            {   
                'selector': {
                    'key': 'selector_itmgrpnam',
                    'type': st.checkbox,
                    'label': 'ItmGrpNam - Κατηγ.',
                    'kwargs': {'value': False},
                },
                'input': {
                    'key': 'input_itmgrpnam',
                    'type': st.multiselect,
                    'dtype': list,
                    'label': 'ItmGrpNam - Κατηγορία',
                    'db_col': 'ItmGrpNam',
                    'kwargs': {'options': df['ItmGrpNam'].unique()},
                },
            },
            {   
                'selector': {
                    'key': 'selector_firmcode',
                    'type': st.checkbox,
                    'label': 'FirmCode - Κατασκ.',
                    'kwargs': {'value': False},
                },
                'input': {
                    'key': 'input_firmcode',
                    'type': st.multiselect,
                    'dtype': list,
                    'label': 'FirmCode - Κατασκευαστής',
                    'db_col': 'FirmCode',
                    'kwargs': {'options': df['FirmCode'].unique()},
                },
            },
            {   
                'selector': {
                    'key': 'selector_usex',
                    'type': st.checkbox,
                    'label': 'U_Sex - Φύλο',
                    'kwargs': {'value': False},
                },
                'input': {
                    'key': 'input_usex',
                    'type': st.multiselect,
                    'dtype': list,
                    'label': 'Select sex - Επιλογή φύλου (1=Ανδρ., 2=Γυν.)',
                    'db_col': 'U_Sex',
                    'kwargs': {'options': df['U_Sex'].unique()},
                },
            },
            {
                'selector': {
                    'key': 'selector_usleeve',
                    'type': st.checkbox,
                    'label': 'U_Sleeve',
                    'kwargs': {'value': False},
                },
                'input': {
                    'key': 'input_usleeve',
                    'type': st.multiselect,
                    'dtype': list,
                    'label': 'Select sleeve - Επιλογή για μανίκι (1=Αμάν., 2=Κοντομ.)',
                    'db_col': 'U_Sleeve',
                    'kwargs': {'options': df['U_Sleeve'].unique()},
                },
            },
            {
                'selector': {
                    'key': 'selector_synth',
                    'type': st.checkbox,
                    'label': 'U_Synth',
                    'kwargs': {'value': False},
                },
                'input': {
                    'key': 'input_synth',
                    'type': st.multiselect,
                    'dtype': list,
                    'label': 'Select composition - Επιλογή σύνθεσης (1=Βαμβ.)',
                    'db_col': 'U_Synth',
                    'kwargs': {'options': df['U_Synth'].unique()},
                },
            },
            {
                'selector': {
                    'key': 'selector_web',
                    'type': st.checkbox,
                    'label': 'Web',
                    'kwargs': {'value': False},
                },
                'input': {
                    'key': 'input_web',
                    'type': st.multiselect,
                    'dtype': list,
                    'label': 'Select Web',
                    'db_col': 'Web',
                    'kwargs': {'options': df['Web'].unique()},
                },
            },
        ]

def render_selectors(ui_spec):
    field_cols = st.columns([1]*len(ui_spec))
    for i, spec in enumerate(ui_spec):
        selector = spec['selector']
        with field_cols[i]:
            selector['type'](selector['label'], key=selector['key'], **selector['kwargs'])

def get_selector_values(ui_spec):
    values = {}
    for spec in ui_spec:
        selector = spec['selector']
        values[selector['key']] = {
            'label': selector['label'], 
            'value': st.session_state[selector['key']],
        }
    return values

def render_inputs(ui_spec, selector_values):
    for spec in ui_spec:
        input = spec['input']
        selector_value = selector_values[spec['selector']['key']]['value']
        if selector_value == True:
            input['type'](input['label'], key=input['key'], **input['kwargs'])

def get_input_values(ui_spec, selector_values):
    values = {}
    for spec in ui_spec:
        input = spec['input']
        selector_value = selector_values[spec['selector']['key']]['value']
        if selector_value == True:
            values[input['key']] = {
                'label': input['label'], 
                'db_col': input['db_col'], 
                'value': st.session_state[input['key']],
                'dtype': input['dtype'],
            }
    return values

st.subheader('Filter fields selection - Επιλογή πεδίων/φίλτρων')
render_selectors(UI_SPECIFICATION)
selector_values = get_selector_values(UI_SPECIFICATION)
# st.write(selector_values)

st.subheader('Filter field inputs - Εισαγωγή κριτηρίων στα επιλεγμένα πεδία')
render_inputs(UI_SPECIFICATION, selector_values)
input_values = get_input_values(UI_SPECIFICATION, selector_values)
# st.write(input_values)

def build_query(input_values, logical_op, compare_op):
    query_frags = []
    for k, v in input_values.items():
        if v['dtype'] == list:
            query_frag_expanded = [f"{v['db_col']} {compare_op} '{val}'" for val in v['value']]
            query_frag = f' {logical_op} '.join(query_frag_expanded)
        elif v['dtype'] == int or v['dtype'] == float:
            query_frag = f"{v['db_col']} {compare_op} {v['dtype'](v['value'])}"
        elif v['dtype'] == str:
            query_frag = f"{v['db_col']}.str.contains('{v['dtype'](v['value'])}')"
        else:
            query_frag = f"{v['db_col']} {compare_op} '{v['dtype'](v['value'])}')"
        query_frags.append(query_frag)
    query = f' {logical_op} '.join(query_frags)
    return query

def display_results(df_results):
    st.write(df_results)

st.subheader('Query builder - Δημιουργία ερωτήματος')

def configure_query():
    c1, c2, _ = st.columns([1,1,2])
    with c1:
        logical_op = st.selectbox('Logical operator', options=['and', 'or'], index=1)
    with c2:
        compare_op = st.selectbox('Comparator operator', options=['==', '>', '<', '<=', '>='], index=0)
    return logical_op, compare_op

logical_op, compare_op = configure_query()
query = build_query(input_values, logical_op, compare_op)

if st.checkbox('Show filter query - Προβολή κριτηρίων ερωτήματος', True):
    st.write(f'Query - Ερώτημα: `{query}`')
st.markdown('---')
if st.button("🔍 Apply filter query"):
    df_results = df.query(query, engine='python') 
    st.subheader('Filtered data results')
    display_results(df_results)
    # count no. of lines
    st.write("Number of lines present:-", 
      len(df_results))

    df_results.to_csv('data/df_results.csv', index=False)
    st.markdown('Filtered data results saved to df_results.csv')

    # download def   
    @st.cache
    def convert_df(df_results):
        return df_results.to_csv(index=False, sep = ';').encode('utf-8')
        
    csv1 = convert_df(df_results)
    
   
    # download csv file users.csv
    st.download_button(
    label="Download data as df_results.csv",
    data=csv1,
    file_name='df_results',
    mime='text/csv',
    )