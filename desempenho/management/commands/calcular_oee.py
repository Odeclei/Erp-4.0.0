from datetime import date, timedelta
from django.core.management.base import BaseCommand, CommandError
from desempenho.services import DesempenhoService
from rule.models import Machines, Group


class Command(BaseCommand):
    help = "Calcula indicadores de desempenho OEE para máquinas, setores e grupos"

    def add_arguments(self, parser):
        parser.add_argument(
            "--data",
            type=str,
            help="Data no formato YYYY-MM-DD (default: hoje)",
            default=None,
        )
        parser.add_argument(
            "--dias",
            type=int,
            help="Calcular para os últimos N dias",
            default=None,
        )
        parser.add_argument(
            "--maquina",
            type=int,
            help="ID de máquina específica",
            default=None,
        )
        parser.add_argument(
            "--grupo",
            type=int,
            help="ID de grupo específico",
            default=None,
        )

    def handle(self, *args, **options):
        try:
            # Determinar data(s)
            if options["dias"]:
                datas = [
                    date.today() - timedelta(days=i)
                    for i in range(options["dias"])
                ]
                datas.reverse()
            elif options["data"]:
                try:
                    datas = [datetime.strptime(options["data"], "%Y-%m-%d").date()]
                except ValueError:
                    raise CommandError("Formato de data inválido. Use YYYY-MM-DD")
            else:
                datas = [date.today()]

            self.stdout.write(
                self.style.SUCCESS(f"Processando {len(datas)} data(s)...")
            )

            for data in datas:
                self.stdout.write(f"\n📅 Data: {data.strftime('%d/%m/%Y')}")

                # Processar máquinas específica ou todas
                if options["maquina"]:
                    try:
                        machine = Machines.objects.get(pk=options["maquina"])
                        DesempenhoService.calcular_indicadores_maquina(machine, data)
                        self.stdout.write(
                            self.style.SUCCESS(f"  ✓ Máquina {machine.code} calculada")
                        )
                    except Machines.DoesNotExist:
                        raise CommandError(f"Máquina ID {options['maquina']} não encontrada")
                else:
                    count = DesempenhoService.calcular_indicadores_todas_maquinas(data)
                    self.stdout.write(
                        self.style.SUCCESS(f"  ✓ {count} máquinas calculadas")
                    )

                # Processar grupos específico ou todos
                if options["grupo"]:
                    try:
                        grupo = Group.objects.get(pk=options["grupo"])
                        DesempenhoService.calcular_resumo_grupo(grupo, data)
                        self.stdout.write(
                            self.style.SUCCESS(f"  ✓ Grupo {grupo.name} calculado")
                        )
                    except Group.DoesNotExist:
                        raise CommandError(f"Grupo ID {options['grupo']} não encontrado")
                else:
                    count = DesempenhoService.calcular_resumos_todos_grupos(data)
                    self.stdout.write(
                        self.style.SUCCESS(f"  ✓ {count} grupos calculados")
                    )

            self.stdout.write(
                self.style.SUCCESS("\n✅ Cálculo de desempenho concluído!")
            )

        except CommandError as e:
            self.stdout.write(self.style.ERROR(f"❌ Erro: {str(e)}"))
            raise
