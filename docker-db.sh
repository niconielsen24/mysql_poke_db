docker run -d \
  --name mysql-pokemons \
  -p 3306:3306 \
  -e MYSQL_ROOT_PASSWORD=nicanor24 \
  -v $PWD/data:/var/lib/mysql \
  mysql
