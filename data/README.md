# Data

El Dataset que se va a utilizar contiene los datos de transacciones de ventas de una tienda de comercio electrónico con sede en el Reino Unido. Esta tienda de Londres vende regalos y artículos para el hogar y sus clientes provienen de todo el mundo.

El conjunto de datos contiene 500.000 Filas y 8 columnas en las cuales esta representadas las transacciones de ventas de la tienda durante un año. Las columnas son las siguientes:

- **TransactionNo** (categórico): un número único de seis dígitos que define cada transacción. La letra “C” en el código indica una cancelación.

- **Date** (numérico): la fecha en que se generó cada transacción.

- **ProductNo** (categórico): un carácter único de cinco o seis dígitos que se utiliza para identificar un producto específico.

- **Product** (categórico): nombre del producto/artículo.

- **Price** (numérico): el precio de cada producto por unidad en libras esterlinas (£).

- **Quantity** (numérico): la cantidad de cada producto por transacción. Valores negativos relacionados con transacciones canceladas.

- **CustomerNo** (categórico): un número único de cinco dígitos que define a cada cliente.

- **Country** (categórico): nombre del país donde reside el cliente.

Hay un pequeño porcentaje de cancelación de pedidos en el conjunto de datos. La mayoría de estas cancelaciones se debieron a condiciones de falta de existencias en algunos productos. En esta situación, los clientes tienden a cancelar un pedido porque quieren que todos los productos se entreguen de una vez.

Este dataset se obtuvo de [kaggle](https://www.kaggle.com/datasets/gabrielramos87/an-online-shop-business). 