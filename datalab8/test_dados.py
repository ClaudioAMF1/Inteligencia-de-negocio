"""Verificações dos critérios de análise e da extração do recorte preservado."""
import importlib.util
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("etl", RAIZ / "scripts/11_prepara_dados_datalab8.py")
etl = importlib.util.module_from_spec(spec)
spec.loader.exec_module(etl)


class DadosAPINFO(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dados = []
        for uf in etl.LOCAIS:
            cls.dados.extend(etl.extrair(etl.BRUTOS / f"p25sal-{uf.lower()}.html", uf))
        cls.resumo, cls.pares, cls.estados = etl.calcular(cls.dados)

    def test_separadores_e_ausencia(self):
        self.assertEqual(etl.numero("8.277"),8277)
        self.assertEqual(etl.numero("12.345,67"),12345.67)
        self.assertIsNone(etl.numero(""))
        with self.assertRaises(ValueError):etl.numero("a combinar")

    def test_preservacao_do_recorte(self):
        self.assertEqual(len(self.dados),664)
        self.assertEqual(sum(r["salario_mensal_brl"] is None for r in self.dados),8)
        chaves={(r["uf"],r["perfil"],r["vinculo_fonte"]) for r in self.dados}
        self.assertEqual(len(chaves),664)
        self.assertEqual(len({r["perfil"] for r in self.dados if r["uf"]=="BR"}),83)

    def test_origem_e_classificacao(self):
        python=next(r for r in self.dados if r["uf"]=="BR" and r["perfil"]=="Programador - Python" and r["vinculo_fonte"]=="CLT")
        self.assertEqual(python["especialidade_original"],"Phyton")
        self.assertEqual(python["salario_mensal_brl"],5365)
        bolsa=next(r for r in self.dados if r["uf"]=="BR" and r["cargo"]=="Estagiário" and r["vinculo_fonte"]=="PJ")
        self.assertEqual(bolsa["natureza"],"bolsa_estagio")
        self.assertIsNone(bolsa["salario_mensal_brl"])

    def test_indicadores_nacionais(self):
        self.assertAlmostEqual(self.resumo["media_referencias_brasil"],8535.481707317073,places=8)
        self.assertEqual(self.resumo["lider"]["perfil"],"Gerente de TI")
        self.assertEqual(self.resumo["maior_referencia"]["salario_mensal_brl"],21007)
        self.assertEqual(self.resumo["menor_referencia"]["salario_mensal_brl"],1757)
        self.assertEqual(self.resumo["menor_sem_bolsa"]["salario_mensal_brl"],2047)
        nacional,_,_=etl.calcular([r for r in self.dados if r["uf"]=="BR"]+[
            {**r,"salario_mensal_brl":r["salario_mensal_brl"]*2 if r["salario_mensal_brl"] is not None else None}
            for r in self.dados if r["uf"]!="BR"])
        self.assertEqual(nacional["media_referencias_brasil"],self.resumo["media_referencias_brasil"])

    def test_pares_e_percentuais(self):
        self.assertEqual(len(self.pares),81)
        self.assertFalse(any(r["perfil"] in ["Estagiário","Assistente de Informática"] for r in self.pares))
        self.assertAlmostEqual(self.resumo["ganho_pj_medio_pct"],27.52740513439945,places=9)
        self.assertAlmostEqual(self.resumo["razao_das_medias_pares_pct"],27.287750363884445,places=9)

    def test_comparacao_equivalente_e_extremos(self):
        self.assertEqual(len(self.estados),24)
        linha=next(r for r in self.estados if r["cargo"]=="Gerente de TI" and r["vinculo"]=="PJ" and r["uf"]=="SP")
        self.assertEqual(linha["salario_estado_brl"],22185)
        self.assertEqual(linha["referencia_brasil_brl"],21007)
        self.assertAlmostEqual(linha["diferenca_pct"],1178/21007*100,places=10)
        self.assertEqual(self.resumo["maior_base_coletada"]["uf"],"SP")
        self.assertEqual(self.resumo["menor_base_coletada"]["salario_mensal_brl"],1555)


if __name__=="__main__":
    unittest.main()
