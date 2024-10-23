<img src="./img/metro_madrid.jpg" alt="drawing" width="500"/>

:es: [Spanish version below!](#Transporte-y-renta:-desigualdad-en-Madrid)

# :uk: / :us: Transport and Income: Inequality in Madrid

## Summary
This project aims to analyse the behaviour on the election of the means of transport by the citizens of the Community of Madrid, studying possible links to their income. Do the higher-income citizens income move themselves across the province in a different manner that those with lower income? Can we find any patterns on different socioeconomic conditions?

The main source is the [Survey of Mobility of 2018](https://datos.comunidad.madrid/dataset/resultados-edm2018), made by Consorcio Regional de Transportes de Madrid (CRTM) from February to June 2018. From here, data of both the respondents and their trips is extracted and analysed .

The income is a constructed indicator, which is assigned by linking the mean income of the known socioeconomic conditions. The data used for this issue is the [Survey of Life Conditions](https://www.madrid.org/iestadis/fijas/estructu/sociales/iecv19.htm), from Madrid's Institue of Statistics.

Finally, there is also a study on whether the weather conditions affect the behaviour of the citizens' trips. All meteorological data is extracted from [AEMET](https://opendata.aemet.es/centrodedescargas/inicio), the Spanish Agency of Meteorology.

The study is focused on **workers'** behaviour on **dry** days and, although most socioeconomic conditions are taken into account, this analysis targets the differences between **men** and **women**.

## Main resources and libraries
The results of the analysis are shown on different media:
+ The [work journal](work_journal.ipynb), where a comprehensive walkthrough of the project is given.
+ A [presentation](media/ENG_EDA_Transp_Madrid.pdf) where the key information can be found.
+ A [Power BI Dashboard](media/dashboard.pbix), which may be used as a fast and interactive way of exploring the main data used by the project.

The versions of the languages and libraries used are:
+ Python: 3.12.5
+ Numpy: 2.1.1
+ Pandas: 2.2.3
+ Matplotlib: 3.9.2
+ Seaborn: 0.13.2


## Hypotheses
The main aim of this project, as presented above, is to prove that **there is a connection between the preferred mode of transport of the citizens and their income** in the Community of Madrid. Some other aspects are tested throughout the study:
+ Higher-income users choose the car as a first transportation option when they go to work.
+ Therefore, lower-income workers use the different modes of public transport.
+ Women use public transport more frequently than men, when going to work.
    + This case is discussed both taken into account their income; and isolating this variable.
+ Weather has little impact on the workers' behaviour when going to work.

## Assumptions
There are some points that have to be taken into account through the analysis:
+ The data by the CRTM is the latest available, but the survey was conducted during 2018.
    + The usage of the whole network covered by CRTM on 2022 was at [85.1 % compared to 2019](https://www.crtm.es/media/4eedagri/informe_anual_2022_eng.pdf), prior to the impact of COVID-19. We assume that the numbers will be similar by the time of making this project (October 2024) and that there hasn't been any deep change on the behaviour of the users because of it.
+ The real income from the users is unknown to us. As it is a constructed indicator (as explained above), it is important to point out:
    + **Income is not wealth**. Wealth is a much more complicated and obscure indicator. We must take into account that this analysis won't cover, for example, citizens with low income but high wealth (which may behave similarly to those with high income or not).
    + The Survey of Life Conditions publishes the **main** income, which is the used data to build said indicator.
    + Four socioeconomic conditions are used for this: **Level of education** (4 categories), **gender**(2), **occupation**(5) and **age**(5). This means the constructed indicator will have a maximum of **200 unique values**.
+ Public transport is treated **as a whole**, and possible differences between each mean of public transport aren't discussed in this project.

# :es: 
# Transporte y renta: desigualdad en Madrid

## Resumen
Este proyecto busca arrojar luz sobre los patrones de comportamiento en el transporte de los ciudadanos de la Comunidad de Madrid, estudiando posibles vínculos con su renta. ¿Se mueven de forma diferente los ciudadanos de rentas altas respecto a los de rentas bajas? ¿Podemos encontrar patrones dadas diferentes condiciones socioeconómicas?

La principal fuente de datos del proyecto es la [Encuesta de Movilidad del Consorcio Regional](https://datos.comunidad.madrid/dataset/resultados-edm2018) de Transportes de Madrid (CRTM), realizada en el 2018. De ella se extraen tanto datos de los individuos como de los viajes realizados por ellos, desde febrero a junio de 2018.

La renta es un indicador asignado, construido mediante las condiciones socioeconómicas conocidas de los encuestados. Se asignan pesos mediante índices creados mediante información extraída de la [Encuesta de Condiciones de Vida](https://www.madrid.org/iestadis/fijas/estructu/sociales/iecv19.htm) del Insituto de Estadística de Madrid, para el año 2018.

Por último, se analiza también si las condiciones meteorológicas tienen un efecto sobre los patrones de movilidad de los ciudadanos. Para ello, se extraen datos de [AEMET](https://opendata.aemet.es/centrodedescargas/inicio), mediante su API.

El estudio se centra en el comoportamiento de los **trabajadores** los días **secos** y, aunque se han tenido en cuenta casi todas las variables socioeconómicas conocidas, el análisis se focalizará en las diferencias entre **hombres** y **mujeres**.

## Recursos principales y librerías
Los resultados de este análisis se muestran en diferentes archivos:
+ La [memoria](memoria.ipynb) del proyecto, donde podemos encontrar una guía exhaustiva de los pasos seguidos a lo largo del proyecto.
+ Una [presentación](media/EDA_Transp_Madrid.pdf), donde se muestran los principales resultados y conclusiones del estudio.
+ Un [dashboard](media/dashboard.pbix) de Power BI, una forma rápida e interactiva de explorar los datos utilizados para el proyecto.

Se han utilizado las siguientes versiones de lenguajes y librerías:
+ Python: 3.12.5
+ Numpy: 2.1.1
+ Pandas: 2.2.3
+ Matplotlib: 3.9.2
+ Seaborn: 0.13.2

## Hipótesis
La hipótesis principal de este proyecto, tal y como se presenta arriba, es que **existe una relación entre la renta y el uso del transporte en la Comunidad de Madrid**. En concreto, se buscará contrastar:
+ Si las rentas más altas eligen el coche como primera opción para desplazamientos laborales.
+ Por lo tanto, las rentas bajas trabajadoras utilizan más el transporte público que el coche.
+ Las mujeres utilizan más el transporte público para desplazamientos laborales, sin tener en cuenta la renta.
    + Este caso se discutirá tanto teniendo en cuenta la renta, como aislando esta variable. 
+ La meteorología tiene poco impacto en el comportamiento de los trabajadores a la hora de elegir su modo de transporte.

## Supuestos
Dados los datos utilizados, hemos de tener en cuenta varios puntos:
+ Se está utilizando la última encuesta publicada por el CRTM, del 2018.
    + El uso de toda la red administrada por el CRTM en el 2022 [ya estaba a un 85,1% de los niveles del 2019](https://www.crtm.es/media/rmxhq5c5/informe_anual_2022.pdf), antes del COVID-19. Suponemos que, a fecha de realización del presente análisis (octubre 2024), los niveles serán similares a aquellos pre-pandemia y que no ha habido cambios profundos en el uso del transporte derivados de ella.
+ No contamos con la renta real de los encuestados. Para ello generaremos un dato estimado en función de las condiciones socioeconómicas de los encuestados.
    + **Renta no implica riqueza**. La riqueza es un indicador complejo y muy difícil de estimar, con lo que hemos de tener en cuenta que este análisis no recogerá, por ejemplo, casos con renta baja pero alta riqueza (que pueden comportarse de forma similar a aquellos con renta alta, o no).
    + La Encuesta de Condiciones de Vida publica la renta **media**, que será el dato utilizado para construir dicho indicador.
    + Se utilizan cuatro condiciones socioeconómicas para este: **Nivel de educación** (4 categorías), **género**(2), **ocupación**(5) y **edad**(5). Esto implica que el indicador creado en el proyecto contará con un máximo de **200 valores únicos** 
+ Tratamos todo el transporte público como **un único conjunto**, este estudio no pormenoriza en posibles diferencias entre cada modo de transporte público.