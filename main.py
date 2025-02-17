import requests
import json

class ChatbotTutor:
    def __init__(self, stream=True):
        """Inicializa o tutor usando Ollama no servidor local"""
        self.url = "http://localhost:11434/api/generate"
        self.model = "llama3"
        self.stream = stream
        self.language = "português do Brasil"
    
    def _generate_response(self, prompt: str) -> str:
        """
        Faz a requisição para o Llama 3 através do Ollama
        """
        data = {
            "model": self.model,
            "prompt": f"TUTOR: {prompt}",
            "temperature": 0.5,
            "top_p": 0.65,
            "max_tokens": 200
        }
        
        try:
            response = requests.post(self.url, json=data, stream=self.stream)
            response.raise_for_status()
            
            if not self.stream:
                return response.json().get('response', "Erro ao obter resposta")
            
            full_response = ""
            for chunk in response.iter_lines():
                if chunk:
                    decoded_chunk = json.loads(chunk.decode("utf-8"))
                    text = decoded_chunk.get("response", "")
                    print(text, end="", flush=True)
                    full_response += text
            
            print("\n")
            return full_response
        
        except requests.exceptions.RequestException as e:
            return f"TUTOR: Erro na requisição: {str(e)}"

    def explain_concept(self, concept: str, difficulty: str) -> str:
        """
        Explica um conceito adaptado ao nível do aluno
        """
        prompt = f"Explique o conceito de {concept} para um estudante de nível {difficulty}. Dê a sua resposta em {self.language}."
        return self._generate_response(prompt)

    def generate_problem(self, concept: str, difficulty: str) -> str:
        """
        Gera um problema prático para o aluno
        """
        prompt = f"Gere um problema {difficulty} sobre {concept} para um estudante praticar. Não forneça a resposta, apenas a questão. Dê a sua resposta em {self.language}."
        return self._generate_response(prompt)

    def solve_problem(self, problem: str) -> str:
        """
        Resolve o problema passo a passo
        """
        prompt = f"Resolva o seguinte problema, mostrando uma explicação passo a passo: {problem}. Dê a sua resposta em {self.language}."
        return self._generate_response(prompt)

    def adjust_explanation(self, student_answer: str) -> str:
        """
        Avalia a resposta do aluno e fornece feedback
        """
        prompt = f"A resposta do estudante foi: {student_answer}. Retorne um feedback sobre a resposta do estudante com uma explicação adicional caso seja necessário. Dê a sua resposta em {self.language}."
        return self._generate_response(prompt)

    def tutoring_session(self):
        """
        Executa uma sessão interativa de tutoria com fluxo flexível
        """
        concept = input("TUTOR: Qual assunto você deseja estudar? ")
        difficulty = input("TUTOR: Qual a dificuldade desejada (fácil, médio, difícil)? ")
        print(f"TUTOR: Vamos começar com uma breve explicação sobre {concept}.")
        
        explanation = self.explain_concept(concept, difficulty)
        if not self.stream:
            print(explanation)

        while True:
            user_input = input("TUTOR: O que deseja fazer agora? Você pode pedir um problema, fazer uma pergunta ou encerrar o programa, digitando 'sair'. Digite sua solicitação: ")
            action = self._generate_response(
                f"O aluno disse: '{user_input}'. Classifique esta entrada e responda exatamente no formato '--<classificacao>--', onde 'classificacao' pode ser problema, pergunta ou sair. Exemplo de resposta válida: '--problema--'. Logo, você tem 4 alternativas de respostas:\n'--problema--'\n'--pergunta--'\n'--sair--'\n'não entendi'"
            ).strip().lower()
            
            if "--problema--" in action:
                problem = self.generate_problem(concept, difficulty)
                if not self.stream:
                    print(problem)
                
                student_answer = input("TUTOR: Qual sua resposta para este problema? ")
                feedback = self.adjust_explanation(student_answer)
                if not self.stream:
                    print(feedback)
                
                extra_explanation = input("TUTOR: Você gostaria de uma explicação mais detalhada sobre a solução? (Sim/Não) ")
                if extra_explanation.lower() in ["sim", "s"]:
                    self.solve_problem(problem)
            
            elif "--pergunta--" in action:
                question = input("TUTOR: Qual sua dúvida? ")
                answer = self._generate_response(f"Responda de forma clara e objetiva: {question}. Dê a sua resposta em {self.language}.")
                if not self.stream:
                    print(answer)
            
            elif "--sair--" in action:
                print("TUTOR: Foi um prazer ensinar você! Até a próxima!")
                break
            
            else:
                print("TUTOR: Não entendi, pode reformular sua solicitação?")


def main():
    print("TUTOR: Olá! Sou seu tutor de álgebra. Podemos conversar sobre qualquer conceito que você quiser aprender. Basta perguntar!")
    
    try:
        tutor = ChatbotTutor()
        
        while True:
            tutor.tutoring_session()
            
            flag = input("TUTOR: Deseja continuar estudando? (Sim/Não): ")
            if flag.lower() in ["não", "nao"]:
                print("TUTOR: Até a próxima!")
                break
    
    except Exception as e:
        print(f"\nTUTOR: Erro: {str(e)}")

if __name__ == "__main__":
    main()
