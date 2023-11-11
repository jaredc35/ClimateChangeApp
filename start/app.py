from shiny import App, render, ui, reactive
import pandas as pd
from pathlib import Path
from shinywidgets import output_widget, register_widget, reactive_read
import ipyleaflet as L
from plot_funs import plot_country, plot_world
from asyncio import sleep
# Get temperature data frame
temperatures = pd.read_csv(Path(__file__).parent/"temperatures.csv")


# Values for dropdown
countries = temperatures['Country'].unique().tolist()

# Values for slider
temp_years =  temperatures['Year'].unique()
temp_year_min = temp_years.min()
temp_year_max = temp_years.max()

# CSS 
font_style = 'font-weight: 100'


app_ui = ui.page_fluid(
    ui.h2("Climate Change", style=font_style),
    ui.row(
        ui.column(6, ui.input_select(id='country', label="Choose a Country", choices=countries, 
                                     selected="United States of America")),

        ui.column(6, 
                ui.row(
                        ui.column(6,ui.input_slider(id='year', label="Choose a Year", min=temp_year_min, 
                                     max=temp_year_max, value=temp_year_min, step=1, animate=False)),
                        ui.column(6, ui.output_ui('color_map')),
                      
                    )
    )
),
    ui.row(
        ui.column(6, ui.output_plot('graph_country')),
        ui.column(6, output_widget('map')),
    ),
    ui.br(),
    ui.row(
        ui.column(6, ui.h5('Imprint', style=font_style)),
        ui.column(6, ui.p("Learn How this app is developed at the following course:", style=font_style))
    ),
    ui.row(
        ui.column(6, ui.row(
            ui.column(2, ui.img(src="developer.png", width="32px"), style="text-align: center"),
            ui.column(10, ui.p("Jared Conway", style=font_style)),
        ),
          ui.row(
                ui.column(2, ui.img(src="address2.png", width="32px"), style="text-align: center;"),
                ui.column(10, ui.p('Somewhere in America', style = font_style))
                ),ui.row(
                ui.column(2, ),
                ui.column(10, ui.p('Street Number Here', style = font_style))
                ),
                ui.row(
                ui.column(2, ),
                ui.column(10, ui.p('USA', style = font_style))
                ),
                      ui.row(
                ui.column(2, ui.img(src="mail2.png", width="32px"), style="text-align: center;"),
                ui.column(10, ui.a(ui.p('jaredt.conway@gmail.com'), href="mailto:jaredt.conway@gmail.com", style = font_style))
                ),
    ),
    ui.column(6, ui.a(ui.img(src='course_logo_300x169.png'), href="https://www.udemy.com" ), style='text-align:center')
    ), style='background-color: #fff'
)


def server(input, output, session):
    
    map = L.Map(center=(0,0), zoom=1)
    # Add a distance scale
    map.add_control(L.leaflet.ScaleControl(position='bottomleft'))
    register_widget('map', map) #References map object from UI to map in line above


    # When year changes, update map's zoom attribute
    @reactive.Effect
    def _():
        layer = plot_world(temp=temperatures, year=input.year())
        map.add_layer(layer)

    @output
    @render.plot
    async def graph_country():
        with ui.Progress(min=1, max=15) as p:
            p.set(message="Calculation in progress", 
                  detail="Please wait...")
            for i in range(1,15):
                p.set(i, message="Computing")
                await sleep(0.1)
        g = plot_country(temp=temperatures, 
                         country=input.country(), year=input.year())
        return g
    
    @output
    @render.ui
    def color_map():
        img = ui.img(src='colormap.png')
        return img

www_dir = Path(__file__).parent/"www"
app = App(app_ui, server, static_assets=www_dir)