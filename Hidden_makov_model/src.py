
import numpy as np
from typing import List, Tuple

class SimpleWeatherHMM:
    
    
    def __init__(self):
        
        self.states = ['Sunny', 'Rainy']
        self.n_states = 2
        
        
        self.observations = ['Happy', 'Sad']
        self.n_obs = 2
        
      
        
        self.A = np.array([
            [0.8, 0.2],  
            [0.4, 0.6]   
        ])
        
       
        self.B = np.array([
            [0.9, 0.1],  
            [0.3, 0.7]   
        ])
        
       
        self.pi = np.array([0.6, 0.4]) 
    
    def generate_sequence(self, days: int) -> Tuple[List[str], List[str]]:
       
        weather_seq = []
        mood_seq = []
        
        
        current_weather = np.random.choice([0, 1], p=self.pi)
        
        for _ in range(days):
            weather_seq.append(self.states[current_weather])
            
            
            mood = np.random.choice([0, 1], p=self.B[current_weather])
            mood_seq.append(self.observations[mood])
            
            
            current_weather = np.random.choice([0, 1], p=self.A[current_weather])
        
        return weather_seq, mood_seq
    
    def viterbi(self, moods: List[str]) -> List[str]:
        
        T = len(moods)
        
        
        mood_idx = [0 if m == 'Happy' else 1 for m in moods]
        
        
        dp = np.zeros((T, 2))
      
        back = np.zeros((T, 2), dtype=int)
        
        
        dp[0][0] = self.pi[0] * self.B[0][mood_idx[0]]  
        dp[0][1] = self.pi[1] * self.B[1][mood_idx[0]] 
        
        
        for t in range(1, T):
            for curr_state in [0, 1]:  
               
                prob_from_sunny = dp[t-1][0] * self.A[0][curr_state] * self.B[curr_state][mood_idx[t]]
                prob_from_rainy = dp[t-1][1] * self.A[1][curr_state] * self.B[curr_state][mood_idx[t]]
                
                
                if prob_from_sunny > prob_from_rainy:
                    dp[t][curr_state] = prob_from_sunny
                    back[t][curr_state] = 0 
                else:
                    dp[t][curr_state] = prob_from_rainy
                    back[t][curr_state] = 1  
        
       
        if dp[T-1][0] > dp[T-1][1]:
            best_path = [0]
        else:
            best_path = [1]
        
    
        for t in range(T-1, 0, -1):
            best_path.insert(0, back[t][best_path[0]])
        
    
        return ['Sunny' if s == 0 else 'Rainy' for s in best_path]
    
    def probability(self, moods: List[str]) -> float:
        
        T = len(moods)
        mood_idx = [0 if m == 'Happy' else 1 for m in moods]
        
        
        alpha = np.zeros((T, 2))
        
        
        alpha[0][0] = self.pi[0] * self.B[0][mood_idx[0]]
        alpha[0][1] = self.pi[1] * self.B[1][mood_idx[0]]
        
        for t in range(1, T):
            for curr in [0, 1]:
                alpha[t][curr] = (alpha[t-1][0] * self.A[0][curr] + 
                                  alpha[t-1][1] * self.A[1][curr]) * self.B[curr][mood_idx[t]]
        
        return alpha[T-1][0] + alpha[T-1][1]


def main():
    
    

    model = SimpleWeatherHMM()
    
    print("=" * 50)
    print("SIMPLE WEATHER HIDDEN MARKOV MODEL")
    print("=" * 50)
    
  
    print("\n--- MODEL PARAMETERS ---")
    print(f"States: {model.states}")
    print(f"Observations: {model.observations}")
    
    print("\nTransition Matrix (Weather change probabilities):")
    print("          Next: Sunny  Rainy")
    print(f"Current Sunny:  {model.A[0][0]:.1f}     {model.A[0][1]:.1f}")
    print(f"Current Rainy:  {model.A[1][0]:.1f}     {model.A[1][1]:.1f}")
    
    print("\nEmission Matrix (Mood given weather):")
    print("                Happy   Sad")
    print(f"  When Sunny:    {model.B[0][0]:.1f}     {model.B[0][1]:.1f}")
    print(f"  When Rainy:    {model.B[1][0]:.1f}     {model.B[1][1]:.1f}")
    

    print("\n" + "=" * 50)
    print("EXAMPLE: GENERATING 7 DAYS")
    print("=" * 50)
    
    true_weather, observed_moods = model.generate_sequence(7)
    
    print("\nDay | True Weather | Observed Mood")
    print("-" * 35)
    for day, (weather, mood) in enumerate(zip(true_weather, observed_moods), 1):
        print(f"{day:3} | {weather:11} | {mood}")
    

    print("\n" + "=" * 50)
    print("PREDICTING WEATHER FROM MOODS ONLY")
    print("=" * 50)
    
    predicted_weather = model.viterbi(observed_moods)
    
    print("\nDay | True Weather | Predicted | Correct?")
    print("-" * 45)
    correct = 0
    for day, (true, pred) in enumerate(zip(true_weather, predicted_weather), 1):
        is_correct = true == pred
        correct += is_correct
        print(f"{day:3} | {true:11} | {pred:9} | {'' if is_correct else 'x'}")
    
    accuracy = correct / len(true_weather)
    print(f"\nAccuracy: {accuracy:.0%}")
    
    print("\n" + "=" * 50)
    print("WHAT IF SCENARIOS")
    print("=" * 50)
    
    test_cases = [
        (['Happy', 'Happy', 'Happy'], "Three happy days"),
        (['Sad', 'Sad', 'Sad'], "Three sad days"),
        (['Happy', 'Sad', 'Happy'], "Alternating moods"),
    ]
    
    for moods, description in test_cases:
        prob = model.probability(moods)
        weather = model.viterbi(moods)
        print(f"\n{description}:")
        print(f"  Observed moods: {moods}")
        print(f"  Most likely weather: {weather}")
        print(f"  Probability of this mood sequence: {prob:.4f}")
    
    print("\n" + "=" * 50)
    print("PREDICTION DEMO")
    print("=" * 50)
    
    print("\nIf you feel HAPPY today, what's the weather?")
    print("  Most likely: Sunny (90% chance of Happy when Sunny)")
    
    print("\nIf you feel SAD today, what's the weather?")
    print("  Most likely: Rainy (70% chance of Sad when Rainy)")
    
    print("\nIf you were HAPPY yesterday and SAD today:")
    result = model.viterbi(['Happy', 'Sad'])
    print(f"  Most likely weather sequence: {result[0]} → {result[1]}")


if __name__ == "__main__":
    main()