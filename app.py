# Importando bibliotecas a serem utilizadas
import streamlit as st      			 			  # Produção simples de pag WEB
import pandas as pd  					  					# Utilizado para trabalhar com planilhas
import plotly.express as px 			  			# Utilizado para gráficos
import plotly.graph_objects as go      	  # gráficos
from plotly.subplots import make_subplots # subplots
from datetime import datetime, timedelta  # (+|-) datas

#Barra lateral
with st.sidebar:
	#Adicionar texto dizendo que é um projeto de TCC
	st.header("Sobre")
	st.markdown('''
		O presente projeto foi realizado como parte do projeto de TCC:
		\"**Sistema para Monitoramento de Desempenho de Painéis Fotovoltaicos Residenciais**\"
		que tem como objetivo  estruturar um sistema para monitoramento de desempenho de painéis fotovoltaicos residenciais,
		conjuntamente com uma revisão dos materiais publicados existente sobre o tema com o fim de melhor modelar o sistema,
		além de apresentar a produção de energia elétrica Fotovoltaica como uma opção viável para o território brisileiro.
		\n
		Discente: Rejane Nobre Bezerra\n
		Prof. Orientador: Luiz Affonso
		''')

# Importando o DataFrame df_iSolar
with st.spinner('Por favor, aguarde...'):
		df_iSolar = pd.read_excel('iSolar.xlsx')
		df_iSolar['Horário'] = pd.to_datetime(df_iSolar['Horário'])
		df_iSolar.set_index("Horário", inplace = True)

# Na pagina principal
st.header('Sistema para Monitoramento de Desempenho de Painéis Fotovoltaicos Residenciais')

st.subheader("Opções")

# ---- Personalização do Usuário - Parte 1 ----
row1col1, row1col2 = st.columns(2)
with row1col1:
	var_Titulo = st.selectbox("Sistema", ["Potência", "CC" , "CA", "Rendimento", "Geração"])

with row1col2:
	frequencia = st.selectbox("Frequência", ["Horária", "Diaria", "Semanal", "Mensal", "Anual"])


# Título do Gráfico - Parte 1
if(var_Titulo == "Geração"):
	titulo = "Gráfico de " + var_Titulo + " - "
else:
	titulo = "Gráfico de " + var_Titulo + " - Média "

# ---- Definindo frequencia das amostras e título parte 2 ----
if(frequencia == 'Horária'):
  frequencia = 'h'
  X_Title = 'horas'
  titulo = titulo + "Horária"
elif(frequencia == 'Diaria'):
  frequencia = 'd'
  X_Title = 'dias'
  titulo = titulo + "Diária"
elif(frequencia == 'Semanal'):
  frequencia = 'w'
  X_Title = 'semanas'
  titulo = titulo + "Semanal"
elif(frequencia == 'Mensal'):
  frequencia = 'm'
  X_Title = 'meses'
  titulo = titulo + "Mensal"
elif(frequencia == 'Anual'):
  frequencia = 'y'
  X_Title = 'anos'
  titulo = titulo + "Anual"


# ---- Personalização do Usuário - Parte 2 (Calendários) ----
d_max = df_iSolar.index[-1]
d_min = df_iSolar.index[0]

d_i_lable = "Início do período (Mín: " + str(d_min.year) + "/" + str(d_min.month) + "/" + str(d_min.day) + "  " +  str(d_min.hour) + ")"
d_f_lable = "Final do período (Máx: " + str(d_max.year) + "/" + str(d_max.month) + "/" + str(d_max.day) + "  " +  str(d_max.hour) + ")"


row2col1, row2col2 = st.columns(2)
with row2col1:
	d_i = st.date_input(d_i_lable,
	   						value= df_iSolar.index[-1],
	   						min_value= d_min, 
	   						max_value= d_max)
with row2col2:
	d_f = st.date_input(d_f_lable,
	   						value= d_max,
	   						min_value= d_min, 
	   						max_value= d_max)

d_i = pd.Timestamp(d_i)
d_f = pd.Timestamp(d_f)
d_f = d_f.replace(hour=23, minute=59, second=59)

# ---- "Potência" ----
if (var_Titulo == "Potência"):
	var_y = ['Potência CC total(kW)',
	       'Potência ativa total(kW)']

	var_Titulo = var_Titulo + " Média"

	df_iSolar_ = df_iSolar[var_y].resample(frequencia).mean()
	filtro = (df_iSolar_.index >= d_i) & (df_iSolar_.index < d_f)

	# Add traces
	fig = px.line(df_iSolar_[filtro], markers=True)

	fig.update_yaxes(title_text="Potência (kW)")

	fig.update_xaxes(title_text=X_Title)

	fig.update_layout(
	  height=700, width = 1300,
	  title= titulo,
	  legend_title="Parametros")

	fig.update_xaxes(rangeslider_visible=True)
	# Ajustar tamanho
	# Ajustar datas!
	st.plotly_chart(fig, theme=None, use_container_width=True)

# ---- "CC" ----
elif (var_Titulo == "CC"):
	var_y = ['MPPT1(A)', 'MPPT2(A)',
	       'MPPT1(V)', 'MPPT2(V)',
	       'Potência CC total(kW)']

	var_Titulo = var_Titulo + " Média"

	df_iSolar_ = df_iSolar[var_y].resample(frequencia).mean()
	filtro = (df_iSolar_.index >= d_i) & (df_iSolar_.index < d_f)

	fig = make_subplots(rows=3, cols=1,
	                shared_xaxes=True,
	                vertical_spacing=0.02)
	# Add traces
	eixo_x = df_iSolar_[filtro].index

	eixo_y = df_iSolar_[filtro]['MPPT1(A)']
	fig.add_trace(go.Scatter(x=eixo_x, y=eixo_y,
	                  mode='lines+markers',
	                  name='MPPT1(A)',
	                  line=dict(dash="solid",)),
	                  row=1, col=1)

	eixo_y = df_iSolar_[filtro]['MPPT2(A)']
	fig.add_trace(go.Scatter(x=eixo_x, y=eixo_y,
	                  mode='lines+markers',
	                  name='MPPT2(A)',
	                  line=dict(dash='dot')),
	                  row=1, col=1)
	fig.update_yaxes(title_text="Corrente (A)", row=1, col=1)

	eixo_y = df_iSolar_[filtro]['MPPT1(V)']
	fig.add_trace(go.Scatter(x=eixo_x, y=eixo_y,
	                  mode='lines+markers',
	                  name='MPPT1(V)'),
	            	  row=2, col=1)

	eixo_y = df_iSolar_[filtro]['MPPT2(V)']
	fig.add_trace(go.Scatter(x=eixo_x, y=eixo_y,
	                  mode='lines+markers',
	                  name='MPPT2(V)'),
	           		  row=2, col=1)
	fig.update_yaxes(title_text="Tensão (V)", row=2, col=1)

	eixo_y = df_iSolar_[filtro]['Potência CC total(kW)']
	fig.add_trace(go.Scatter(x=eixo_x, y=eixo_y,
	                  mode='lines+markers',
	                  name='Potência CC total(kW)'),
	          		  row=3, col=1)
	fig.update_yaxes(title_text="Potência (kW)", row=3, col=1)
	fig.update_xaxes(title_text=X_Title, row=3, col=1)

	fig.update_xaxes( row=3, col=1, rangeslider_visible=True)

	fig.update_layout(
	  height=800, width = 1300,
	  title= titulo,
	  legend_title="Parametros")

	st.plotly_chart(fig, theme=None, use_container_width=True)


# ---- "CA" ----
elif (var_Titulo == "CA"):
	var_y = ['Corrente da fase A(A)',
	       'Tensão da Fase A(V)',
	       'Potência ativa total(kW)']
	var_Titulo = var_Titulo + " Média"

	df_iSolar_ = df_iSolar[var_y].resample(frequencia).mean()
	filtro = (df_iSolar_.index >= d_i) & (df_iSolar_.index < d_f)

	fig = make_subplots(rows=3, cols=1,
	                shared_xaxes=True,
	                vertical_spacing=0.02)
	# Add traces
	eixo_x = df_iSolar_[filtro].index

	eixo_y = df_iSolar_[filtro]['Corrente da fase A(A)']
	fig.add_trace(go.Scatter(x=eixo_x, y=eixo_y,
	                  mode='lines+markers',
	                  name='Corrente da fase A(A)'),
	            row=1, col=1)
	fig.update_yaxes(title_text="Corrente (A)", row=1, col=1)

	eixo_y = df_iSolar_[filtro]['Tensão da Fase A(V)']
	fig.add_trace(go.Scatter(x=eixo_x, y=eixo_y,
	                  mode='lines+markers',
	                  name='Tensão da Fase A(V)'),
	            row=2, col=1)
	fig.update_yaxes(title_text="Tensão (V)", row=2, col=1)

	eixo_y = df_iSolar_[filtro]['Potência ativa total(kW)']
	fig.add_trace(go.Scatter(x=eixo_x, y=eixo_y,
	                  mode='lines+markers',
	                  name='Potência ativa total(kW)'),
	            row=3, col=1)
	fig.update_yaxes(title_text="Potência (kW)", row=3, col=1)
	fig.update_xaxes(title_text=X_Title, row=3, col=1)
	fig.update_xaxes( row=3, col=1, rangeslider_visible=True)

	fig.update_layout(
	  height=800, width = 1300,
	  title= titulo,
	  legend_title="Parametros")

	st.plotly_chart(fig, theme=None, use_container_width=True)


# ---- "Rendimento" ----
elif (var_Titulo == "Rendimento"):
	var_y = ['Rendimento diário(kWh)']
	var_Titulo = var_Titulo + " Média"

	df_iSolar_ = df_iSolar[var_y].resample(frequencia).mean()
	filtro = (df_iSolar_.index >= d_i) & (df_iSolar_.index < d_f)

	# Add traces
	fig = px.line(df_iSolar_[filtro], markers=True)

	fig.update_yaxes(title_text="Rendimento (kWh)")

	fig.update_xaxes(title_text=X_Title)

	fig.update_layout(
	  height=800, width = 1300,
	  title= titulo,
	  legend_title="Parametros")

	fig.update_xaxes(rangeslider_visible=True)

	st.plotly_chart(fig, theme=None, use_container_width=True)


# ---- "Geração" ----
else:
	var_y = ['Geração de energia total(kWh)']

	df_iSolar_ = df_iSolar[var_y]

	filtro_min = df_iSolar_['Geração de energia total(kWh)'] > 0
	df_iSolar_Max = df_iSolar_[filtro_min].resample(frequencia).max()
	df_iSolar_Min = df_iSolar_[filtro_min].resample(frequencia).min()
	df_iSolar_Min['Geração de energia total(kWh)'][0] = 0
	df_iSolar_ = df_iSolar_Max - df_iSolar_Min

	filtro = (df_iSolar_.index >= d_i) & (df_iSolar_.index < d_f)

	fig = make_subplots(rows=2, cols=1,
	                  shared_xaxes=True,
	                  vertical_spacing=0.02)
	# Add traces
	eixo_x = df_iSolar_[filtro].index
	eixo_y = df_iSolar_[filtro]['Geração de energia total(kWh)']
	fig.add_trace(go.Bar(x=eixo_x, y=eixo_y,
	                        name='Geração de energia total(kWh)'),
	                        row=1, col=1)
	fig.update_yaxes(title_text="Geração (kWh)", row=1, col=1)

	eixo_y = df_iSolar_Max[filtro]['Geração de energia total(kWh)']
	fig.add_trace(go.Scatter(x=eixo_x, y=eixo_y,
	                    mode='lines+markers',
	                    name='Geração de energia total(kWh)'),
	                    row=2, col=1)
	fig.update_yaxes(title_text="Progresso do Acumulo (kWh)", row=2, col=1)

	fig.update_xaxes( row=2, col=1, rangeslider_visible=True)

	fig.update_layout(
	    height=800, width = 1300,
	    title= titulo,
	    legend_title="Parametros")
	fig.update_layout(hovermode="x unified")

	st.plotly_chart(fig, theme=None, use_container_width=True)

for v in var_y:
	st.write("-" * 34) # Linha horizontal de separação
	st.subheader('Mais sobre ' + v)
	
	start = v.find('(') + 1
	end = v.find(')')
	unid = ' ' + v[start:end]

	filtro_metric = (df_iSolar.index >= d_i) & (df_iSolar.index < d_f) & (df_iSolar[v] != 0)
	col1, col2 = st.columns(2)
	with col1:
		max_ = df_iSolar[filtro_metric][v].max()
		#max_ = float(max_)
		max_ = round(max_, 3)
		max_idx = df_iSolar[filtro_metric][v].idxmax()
		
		st.metric(label="Máximo do Periodo", value=str(max_) + unid, delta=str(max_idx))

	with col2:	
		min_ = df_iSolar[filtro_metric][v].min()
		min_ = round(min_, 3)
		min_idx = df_iSolar[filtro_metric][v].idxmin()
		
		st.metric(label="Mínimo do Periodo (>0)", value=str(min_) + unid, delta=str(min_idx))

#Colocar contato abaixo
st.write("-" * 34) # Linha horizontal de separação
st.subheader("Contato")
col1, col2 = st.columns(2)
with col1:
	st.info('Email: rejane.nobre.080@ufrn.edu.br', icon="✉️")
with col2:
	st.info('Github: rejanenobre', icon="💻")

st.info('UFRN - Natal/RN - 2023', icon="🎓", )