import requests
import json
import time
from typing import Dict, List, Optional

class chatbotTutor:
    def __init__(self, stream = True):
        """Inicializa o tutor usando Ollama no servidor local"""
        self.url = "http://localhost:11434/api/generate"
        self.model = "llama2"
        self.stream = stream
    
    def _generate_response(self, prompt: str) -> str:
        """
        Faz a requisição para o Llama 2 através do Ollama
        """
        data = {
            "model": self.model,
            "prompt": prompt,
            "temperature": 0.5,
            "top_p": 0.65,
            "max_tokens": 200
        }
        
        try:
            if not self.stream:
                response = requests.post(self.url, json=data, stream=self.stream)
                response.raise_for_status()
                return response.json()['response']
            else:
                
                response = requests.post(self.url, json=data, stream=True)  # Stream ativado
                response.raise_for_status()

                full_response = ""
                for chunk in response.iter_lines():
                    if chunk:
                        decoded_chunk = json.loads(chunk.decode("utf-8"))  # Decodificando JSON
                        text = decoded_chunk.get("response", "")
                        print(text, end="", flush=True)  # Exibe no terminal sem quebrar linha
                        full_response += text

                print("\n")  # Adiciona quebra de linha após resposta completa
                return full_response

        except requests.exceptions.RequestException as e:
            return f"Erro na requisição: {str(e)}"

    def explain_concept(self, concept: str, level: str) -> str:
        """
        Explica um conceito algébrico adaptado ao nível do aluno
        """
        prompt = f"Explique o conceito de {concept} para um estudante de nível {level}. Dê a sua resposta em português do Brasil."
        return self._generate_response(prompt)

    def generate_problem(self, concept: str, difficulty: str) -> str:
        """
        Gera um problema prático para o aluno
        """
        prompt = f"Gere um problema {difficulty} sobre {concept} para um estudante praticar."
        return self._generate_response(prompt)

    def solve_problem(self, problem: str) -> str:
        """
        Resolve o problema passo a passo
        """
        prompt = f"Resolva o seguinte problema, mostrando uma explicação passo a passo: {problem}"
        return self._generate_response(prompt)

    def adjust_explanation(self, student_answer: str, correct_answer: str) -> str:
        """
        Avalia a resposta do aluno e fornece feedback
        """
        prompt = f"A resposta do estudante foi: {student_answer}. A resposta correta é: {correct_answer}.\nRetorne um feedback sobre a resposta do estudante com uma explicação adicional caso seja necessário."
        return self._generate_response(prompt)

    def tutoring_session(self, concept: str, difficulty: str = "fácil"):
        """
        Executa uma sessão interativa de tutoria
        """
        #Explique o conceito
        print("Explicação:")
        explanation = self.explain_concept(concept, difficulty)
        if not self.stream:
            print(explanation)
        
        # Gerar um problema para prática
        print("\nProblema para prática:")
        problem = self.generate_problem(concept, difficulty)
        print(problem)
        
        #Step 3: Receber a resposta do estudante
        student_answer = input("\nSua resposta: ")
        
        # Prover solução correta
        print("\nSolução correta:")
        correct_solution = self.solve_problem(problem)
        print(correct_solution)
        
        # Ajustar explicação baseada na resposta do estudante
        print("\nFeedback:")
        feedback = self.adjust_explanation(student_answer, correct_solution)
        print(feedback)

def main():
    print("Iniciando o Tutor de Álgebra...")
    
    try:
        tutor = chatbotTutor()

        concept = input("Digite o assunto que deseja estudar: ")
        difficulty = input("Digite a dificuldade que deseja: ")

        tutor.tutoring_session(concept, difficulty)
    except Exception as e:
        print(f"\nErro: {str(e)}")

if __name__ == "__main__":
    main()