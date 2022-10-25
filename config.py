# Таймаут - параметр отвечающий за время ожидания загрузки веб-сайта, объясняя проще
# этот параметр задаёт количество времени которое программа будет ждать чтобы сайт загрузился
# если сайт в течении этого времени не загрузиться, то он будет считаться недоступным либо заблокированным.
# Стандартное значение Таймаута - 5 сек.
# Параметр очень важен, поскольку у разных операторов разная скорость интернета, вдруг идет проверка по 3г , где сайты в среднем грузяться 8 сек.

timeout_cf_443 = 5
timeout_cf_80 = 5
timeout_fastly_443 = 5
timeout_fastly_80 = 5
timeout_azure_443 = 5
timeout_azure_80 = 5
timeout_cfront_443 = 5
timeout_cfront_80 = 5
timeout_arvan_443 = 5
timeout_arvan_80 = 5
timeout_verizon_443 = 5
timeout_verizon_80 = 5

