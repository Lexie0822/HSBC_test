# Property Market Analysis Service

This Spring Boot application exposes aggregate statistics of the housing dataset via a
simple REST API.  It is designed to satisfy the backend requirements of the
"Property Market Analysis" application described in the technical assessment.

## Endpoints

| Method | Path         | Description                               |
|-------:|-------------:|-------------------------------------------|
|   GET  | `/health`    | Liveness/readiness check. Returns `{ status: "ok" }`. |
|   GET  | `/statistics`| Returns the total number of properties, average price, minimum price and maximum price. |

Example response:

```json
{
  "count": 50,
  "averagePrice": 264600.0,
  "minPrice": 160000.0,
  "maxPrice": 410000.0
}
```

## Building and running

Prerequisites:

* JDK 21
* Maven 3.8+

To build the project:

```sh
cd analysis_service
mvn package
```

To run the service locally:

```sh
mvn spring-boot:run
```

The service will start on <http://localhost:8080> by default.  You can then access the
statistics endpoint at <http://localhost:8080/statistics>.

## Implementation notes

* The dataset `HousePriceDataset.csv` is bundled under `src/main/resources` and
  loaded at startup.  The service reads through the CSV once to compute the total
  number of rows, the average sale price and the min/max sale prices.  These
  values are stored in memory and served on demand.
* The service uses the OpenCSV library for parsing the CSV file.
