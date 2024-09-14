import unittest
from unittest.mock import patch
from io import StringIO
from movies import filmes, proximo_id, adicionar_filme, mostrar_filmes, buscar_filme, buscar_por_diretor_closure, excluir_filme

class TestAdicionarFilme(unittest.TestCase):
    def setUp(self):
        global filmes, proximo_id
        filmes.clear()
        proximo_id = 1

    @patch('builtins.input', side_effect=['Inception', 'Christopher Nolan', '2010'])
    def test_adicionar_filme_sucesso(self, mock_input):
        global filmes, proximo_id

        adicionar_filme()

        self.assertEqual(len(filmes), 1)
        self.assertEqual(filmes[0]['titulo'], 'Inception')
        self.assertEqual(filmes[0]['diretor'], 'Christopher Nolan')
        self.assertEqual(filmes[0]['ano'], 2010)
        self.assertEqual(filmes[0]['id'], 1)
        # self.assertEqual(proximo_id, 2)

    @patch('builtins.input', side_effect=['', 'Christopher Nolan', '2010'])
    def test_adicionar_filme_titulo_vazio(self, mock_input):
        with self.assertRaises(ValueError):
            adicionar_filme()

    @patch('builtins.input', side_effect=['Inception', '', '2010'])
    def test_adicionar_filme_diretor_vazio(self, mock_input):
        with self.assertRaises(ValueError):
            adicionar_filme()

    @patch('builtins.input', side_effect=['Inception', 'Christopher Nolan', 'abc'])
    def test_adicionar_filme_ano_invalido(self, mock_input):
        with self.assertRaises(ValueError):
            adicionar_filme()

    @patch('builtins.input', side_effect=['Inception', 'Christopher Nolan', '2010'])
    def test_adicionar_filme_repetido(self, mock_input):
        filmes.append({
            'id': 1,
            'titulo': 'Inception',
            'diretor': 'Christopher Nolan',
            'ano': 2010
        })
        adicionar_filme()
        self.assertEqual(len(filmes), 1)

    @patch('sys.stdout', new_callable=StringIO)
    def test_mostrar_filmes(self, mock_stdout):
        filmes.append({
            'id': 1,
            'titulo': 'Inception',
            'diretor': 'Christopher Nolan',
            'ano': 2010
        })

        mostrar_filmes()
        output = mock_stdout.getvalue().strip()
        expected_output = "ID: 1,\n Título: Inception,\n Diretor: Christopher Nolan,\n Ano: 2010"
        self.assertIn(expected_output, output)

    @patch('builtins.input', side_effect=['Inception'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_buscar_filme_sucesso(self, mock_stdout, mock_input):
        filmes.append({
            'id': 1,
            'titulo': 'Inception',
            'diretor': 'Christopher Nolan',
            'ano': 2010
        })

        buscar_filme()
        output = mock_stdout.getvalue().strip()
        expected_output = "ID: 1\n\nTítulo: Inception\n\nDiretor: Christopher Nolan\n\nAno de lançamento: 2010"
        self.assertEqual(output, expected_output)

    @patch('builtins.input', side_effect=['Nonexistent'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_buscar_filme_falha(self, mock_stdout, mock_input):
        buscar_filme()
        output = mock_stdout.getvalue().strip()
        self.assertIn("Filme 'Nonexistent' não encontrado.", output)

    @patch('builtins.input', side_effect=['1'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_excluir_filme_sucesso(self, mock_stdout, mock_input):
        filmes.append({
            'id': 1,
            'titulo': 'Inception',
            'diretor': 'Christopher Nolan',
            'ano': 2010
        })

        excluir_filme()
        self.assertEqual(len(filmes), 0)
        output = mock_stdout.getvalue().strip()
        self.assertIn("Filme com ID 1 excluído com sucesso.", output)

    @patch('builtins.input', side_effect=['2'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_excluir_filme_nao_encontrado(self, mock_stdout, mock_input):
        filmes.append({
            'id': 1,
            'titulo': 'Inception',
            'diretor': 'Christopher Nolan',
            'ano': 2010
        })

        excluir_filme()
        output = mock_stdout.getvalue().strip()
        self.assertIn("Nenhum filme encontrado com o ID 2.", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_buscar_por_diretor_sucesso(self, mock_stdout):
        filmes.append({
            'id': 1,
            'titulo': 'Inception',
            'diretor': 'Christopher Nolan',
            'ano': 2010
        })

        func = buscar_por_diretor_closure('Christopher Nolan')
        func()

        output = mock_stdout.getvalue().strip()
        expected_output = "ID: 1\n\nTítulo: Inception\n\nDiretor: Christopher Nolan\n\nAno de lançamento: 2010"
        self.assertEqual(output, expected_output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_buscar_por_diretor_falha(self, mock_stdout):
        filmes.append({
            'id': 1,
            'titulo': 'Inception',
            'diretor': 'Christopher Nolan',
            'ano': 2010
        })

        func = buscar_por_diretor_closure('Steven Spielberg')
        func()

        output = mock_stdout.getvalue().strip()
        self.assertIn("Nenhum filme encontrado para o diretor 'Steven Spielberg'", output)

if __name__ == '__main__':
    unittest.main()