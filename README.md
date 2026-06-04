# Linux Stack Memory Exhaustion Demo

This example simulates a 'great stack' of applications on Linux by launching multiple Python processes, each consuming significant memory and CPU. It demonstrates how cumulative resource exhaustion can lead to severe system slowdowns and unresponsiveness, an 'engineer panic' scenario, even without a full kernel crash. Observe the performance degradation of a simple task when the simulated services are active.

## Language

`python`

## How to Run

1. Save the code as `main.py`.
2. Run from your terminal: `python main.py`.
3. Observe the performance degradation and system resource usage (e.g., with `htop` or `top` in another terminal) while the script is running.

## Original Article

This example accompanies the Turkish article: [Linux Ortamlarında Büyük Yığınların Çalışmaması: Bir Çekirdek Paniği Değil, Bir Mühendis Paniği](https://fatihsoysal.com/blog/linux-ortamlarinda-buyuk-yiginlarin-calismamasi-bir-cekirdek-panigi-degil-bir-muhendis-panigi/).

## License

MIT — see [LICENSE](LICENSE).
