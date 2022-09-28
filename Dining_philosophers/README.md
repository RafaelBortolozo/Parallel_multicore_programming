# Problema do Jantar dos Filósofos

Considere 5 filósofos que passam a vida a pensar e a comer. Compartilham de uma mesa redonda rodeada por 5 cadeiras sendo que cada uma das cadeiras pertence a um filósofo. No centro da mesa encontra-se uma panela de arroz e estão 5 garfos na mesa, um para cada filósofo.

![Screenshot_4](https://user-images.githubusercontent.com/62819159/192802827-a2f7362e-43c8-432c-9cfa-cbd856659535.png)

Quando um filósofo pensa não interage com os seus colegas. De tempos em tempos, cada filósofo fica com fome e tenta apanhar os dois garfos que estão mais próximos (os garfos que estão ou à esquerda ou à direita). **O filósofo apenas pode apanhar um garfo de cada vez** e como o leitor compreende, **não pode apanhar um garfo se este estiver na mão do vizinho**.

Quando um filósofo esfomeado tem 2 garfos ao mesmo tempo ele come sem largar os garfos. Apenas quando acaba de comer, o filósofo pousa os garfos, libertando-os e começa a pensar de novo. **O nosso objetivo é ter uma representação/implementação que nos permita simular este jantar sem que haja problemas de *deadlock* ou *starvation***.

### Possível solução utilizando semáforo:

Para isso, o jantar poderá ser modelado usando uma *thread* para representar cada filósofo e pode ser utilizado semáforos para representar cada garfo. Quando um filósofo tenta agarrar um garfo executa uma operação *wait* no semáforo, quando o filósofo larga o garfo executa uma operação *release* nesse mesmo semáforo. Cada filósofo (*thread*) vai seguir o algoritmo, ou seja, todos fazem as mesmas ações. As primitivas de sincronização *wait* e *release* são utilizadas para evitar situações de *deadlock*.

Uma outra possibilidade de *deadlock* seria o fato de mais do que um filósofo ficar com fome ao mesmo tempo, os filósofos famintos tentariam agarrar os garfos ao mesmo tempo. **Isso é outro ponto que uma solução satisfatória precisará estar atento**, devendo ser evitado que um filósofo possa morrer de fome. Lembrar que uma solução livre de *deadlock* não elimina necessariamente a possibilidade de um filósofo morrer de fome.

### **Requisitos mínimos do trabalho:**

1. É **obrigatório** contemplar a restrição de **deadlock**, ou seja, a implementação deve resolver (e evitar) o problema de deadlock;
2. É obrigatório contornar o problema de **starvation**. Os filósofos devem ter um tempo máximo aceitável (individualmente) para ficarem sem se alimentar. Este tempo pode ser um parâmetro definido em milissegundos;
3. Nem todas as pessoas se alimentam na mesma velocidade, portanto, cada filósofo deve ter o “seu” tempo necessário para a sua alimentação, que são diferentes uns dos outros.
