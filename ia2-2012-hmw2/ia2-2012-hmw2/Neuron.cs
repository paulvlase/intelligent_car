using System;

namespace ia22012hmw2
{
	public class Neuron
	{
		public Double Output;
		public Double DesiredOutput;
		public Double Error;
		public Double Grad;
		public Double OldGrad;
		public Neuron[] InNeurons;
		public Double[] Weights;
		public Double[] OldWeights;
		public Neuron[] OutNeurons;
		public Neuron[] NeuronNumber;
		Int32 noLayer;
		Int32 noNeuron;
		Boolean outputLayer;

		public Neuron (Int32 noLayer, Int32 noNeuron, Boolean outputLayer)
		{
			this.noLayer = noLayer;
			this.noNeuron = noNeuron;
			this.outputLayer = outputLayer;

			Output = 0.0;
			DesiredOutput = 0.0;
			Error = 0.0;
			Grad = 0.0;
			OldGrad = 0.0;

			InNeurons = null;
			Weights = null;
			OldWeights = null;
			OutNeurons = null;
			NeuronNumber = null;
		}

		public void InitWeights ()
		{
			Random random = new Random ();

			Weights = new Double[InNeurons.Length + 1];
			OldWeights = new Double[InNeurons.Length + 1];

			for (int i = 0; i < Weights.Length; i++) {
				Double weight = random.NextDouble () * 0.05;

				if (random.Next () % 2 == 1) {
					weight = -weight;
				}
				OldWeights [i] = Weights [i] = weight;
			}
		}

		public void Forward ()
		{
			if (InNeurons == null) {
				Console.WriteLine ("ERROR: This is input layer");
				return;
			}

			Double linearCombiner = (-1) * Weights [InNeurons.Length];

			for (int i = 0; i < InNeurons.Length; i++) {
				linearCombiner += Weights [i] * InNeurons [i].Output;
			}
			Output = Activation (linearCombiner);

		}

		public void Gradient ()
		{
			if (outputLayer) {
				Error = DesiredOutput - Output;
			} else {
				Error = 0.0;

				for (int i = 0; i < OutNeurons.Length; i++) {
					Error += OutNeurons [i].Error * OutNeurons [i].Weights [noNeuron];
				}
			}

			Grad = Error * Output * (1.0 - Output);
		}

		public void Back ()
		{
			int i;
			Double old;

			for (i = 0; i < InNeurons.Length; i++) {
				old = Weights [i];

				Weights [i] = Weights [i] + Config.Momentum
						* (Weights [i] - OldWeights [i]) + Config.LearningRate * Grad * InNeurons [i].Output;

				OldWeights [i] = old;
			}

			old = Weights [i];

			Weights [i] = Weights [i] + Config.Momentum
						* (Weights [i] - OldWeights [i]) + Config.LearningRate * Grad * (-1);

			OldWeights [i] = old;
		}

		private Double Activation (Double t)
		{
			return 1.0 / (1.0 + Math.Pow (Math.E, -t));
		}
	}
}

