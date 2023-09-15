suppressPackageStartupMessages(library(arrow))
library(ggplot2)
library(patchwork)
library(Robyn)
library(plumber)
library(jsonlite)

#* Convert hex data back to raw bytes
hex_to_raw <- function(x) {
  chars <- strsplit(x, "")[[1]]
  as.raw(strtoi(paste0(chars[c(TRUE, FALSE)], chars[c(FALSE, TRUE)]), base=16L))
}

#* Serialises a ggplot into a hex string by first converting to png
ggplot_serialize <- function(plot,dpi,width,height) {
  temp_file <- tempfile(fileext = ".png")
  ggsave(temp_file, plot, device = "png", dpi = dpi, width = width, height = height, limitsize = FALSE)
  png_data <- readBin(temp_file, "raw", file.info(temp_file)$size)
  hex_string <- paste0(sprintf("%02x", as.integer(png_data)), collapse = "")
  file.remove(temp_file)
  return(hex_string)
}

#* Whether an object is a named list 
is_named_list <- function(obj) {
  is_list <- is.list(obj)
  has_names <- !is.null(names(obj))
  return(is_list && has_names)
}

#* Determine whether an object is a ggplot
is_ggplot <- function(obj) {
  inherits(obj, "ggplot")
}

#* Iterates recursively and helps to serialise any ggplot objects
recursive_ggplot_serialize <- function(obj,dpi=900,width=12,height=8) {
  for (key in names(obj)) {
    if (is_ggplot(obj[[key]])) {
        obj[[key]] <- ggplot_serialize(obj[[key]],dpi,width,height)
    }
    else if (is_named_list(obj[[key]])) {
        obj[[key]] <- recursive_ggplot_serialize(obj[[key]],dpi,width,height)
    }
  }
  return(obj)
}

#* Fetch prophet data
#* @post /dt_simulated_weekly
function() {
  return(Robyn::dt_simulated_weekly)
}

#* Fetch prophet data
#* @post /dt_prophet_holidays
function() {
  return(Robyn::dt_prophet_holidays)
}


#* Run a model and post back output collect
#* @param modelData Model data feather file in hex format
#* @param jsonInput Additional parameters for robyninputs in json format
#* @param jsonRunArgs Additional parameters for robynrun in json format
#* @param onePagers Build the one pager files
#* @post /robynrun
function(modelData,jsonInput,jsonRunArgs,onePagers=FALSE) {

    dt_input_bytes <- hex_to_raw(modelData)
    dt_input <- arrow::read_feather(dt_input_bytes)
    data("dt_prophet_holidays")

    argsInp <- jsonlite::fromJSON(jsonInput)
    argsRun <- jsonlite::fromJSON(jsonRunArgs)

    InputCollect <- robyn_inputs(
      dt_input = dt_input,
      dt_holidays = dt_prophet_holidays,
      json_file = argsInp
    )

    OutputModels <- do.call(robyn_run, c(list(InputCollect = InputCollect),argsRun))

    OutputCollect <- robyn_outputs(InputCollect, OutputModels,export=FALSE)

    if(onePagers){
      one_pagers <- list()
      for (select_model in OutputCollect$clusters$models$solID) {
        one_pagers[[select_model]] <- recursive_ggplot_serialize(robyn_onepagers(InputCollect, OutputCollect, select_model = select_model, export = FALSE),dpi=900,width=17,height=19)
      }
      OutputCollect$clusters$models$onepagers <- one_pagers
    }

    return(recursive_ggplot_serialize(OutputCollect))

}