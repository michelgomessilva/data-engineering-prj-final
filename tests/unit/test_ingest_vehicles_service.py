from unittest.mock import MagicMock, patch

from application.use_cases.ingest_vehicles import IngestVehiclesService


@patch("application.use_cases.ingest_vehicles.current_date", return_value="mocked_date")
@patch("application.use_cases.ingest_vehicles.get_spark_session")
@patch("application.use_cases.ingest_vehicles.CarrisAPIClient")
@patch("application.use_cases.ingest_vehicles.GenericSparkRepository")
@patch("application.use_cases.ingest_vehicles.ParquetStorage")
@patch("application.use_cases.ingest_vehicles.VehiclesNormalizer")
def test_ingest_should_run_pipeline(
    mock_normalizer,
    mock_storage,
    mock_repo,
    mock_api_client,
    mock_get_spark_session,
    mock_current_date,
):
    # Arrange
    mock_raw_data = [{"id": 1}, {"id": 2}]
    mock_normalized_data = [{"vehicle_id": 1}, {"vehicle_id": 2}]

    mock_api_client.return_value.fetch.return_value = mock_raw_data
    mock_normalizer.normalize.return_value = mock_normalized_data

    mock_df = MagicMock()
    mock_df.count.return_value = 100
    mock_df.withColumn.return_value = mock_df  # encadeamento
    mock_repo.return_value.to_dataframe.return_value = mock_df

    service = IngestVehiclesService()

    # Act
    service.ingest()

    # Assert
    mock_api_client.return_value.fetch.assert_called_once()
    mock_normalizer.normalize.assert_called_once_with(mock_raw_data)
    mock_repo.return_value.to_dataframe.assert_called_once_with(mock_normalized_data)
    mock_storage.return_value.save.assert_called_once()
