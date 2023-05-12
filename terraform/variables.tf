locals {
    data_lake_bucket = "trendba-bucket-1"
}

variable "project" {
  description = "373374964804"
}

variable "region" {
    description = "Region for GCP resources"
    default = "us-west1"
    type = string
}

variable "credentials" {
    description = "Path for Application Default Credentials"
    default = "/Users/garrethlee/.config/gcloud/application_default_credentials.json"
    type = string
}

variable "storage_class" {
    description = "Storage class for bucket"
    default = "STANDARD"
}

variable "BIGQUERY_DATASET" {
    description = "BigQuery Dataset that raw data from GCS will be written to"
    type = string
    default = "all_subreddits_daily"
}

variable "TABLE_NAME" {
    description = "Table in BigQuery containing aggregated data"
    type = string
    default = "nba_subreddits"
}