using System;
using System.Collections.Generic;

namespace ia22012hmw2
{
	public class BackpropagationNetwork
	{
		private Int32 nInputs;
		private Int32 nOutputs;
		private List<Example> dataSet;
		private List<Neuron[]> layers;
		private Neuron[]       inputLayer;
		private Neuron[]       outputLayer;
		private Int32 noTesting;
		private Int32 noValidating;
		private Int32 noLearning;
		public Int32 iter;
		public Double learningMae;
		public Double learningMre;
		public Double testingMae;
		public Double testingMre;

		public BackpropagationNetwork (List<Example> dataSet, Int32 nInputs, Int32 nOutputs)
		{
			this.dataSet = dataSet;

			this.nInputs = nInputs;
			this.nOutputs = nOutputs;

			layers = new List<Neuron[]> ();

			noTesting = (Int32)Math.Floor (dataSet.Count * 1.0 / 3.0);
			noValidating = (Int32)Math.Floor ((dataSet.Count - noTesting) * 1.0 / 3.0);
			noLearning = (Int32)Math.Floor ((Double)dataSet.Count - noValidating - noTesting);
		}

		public void Simulate ()
		{
			BuildNetwork ();
			LearnNetwork ();

			ComputeMeanErrors (0, noLearning + noValidating, ref learningMae, ref learningMre);
			ComputeMeanErrors (noLearning + noValidating, dataSet.Count, ref testingMae, ref testingMre);
		}

		private void BuildNetwork ()
		{
			List<Int16> hiddenLayerNeurons = new List<Int16> ();

			if (Config.firstHiddenLayer != 0) {
				hiddenLayerNeurons.Add (Config.firstHiddenLayer);
			}

			if (Config.secondHiddenLayer != 0) {
				hiddenLayerNeurons.Add (Config.secondHiddenLayer);
			}

			/* Input layer */
			BuildInputLayer ();
			/* Hidden layers. */
			BuildHiddenLayers (hiddenLayerNeurons);
			/* Output layer. */
			BuildOutputLayer ();

			/* Make connections. */
			MakeConnections ();
		}

		private void BuildInputLayer ()
		{
			inputLayer = new Neuron[nInputs];

			for (int j = 0; j < inputLayer.Length; j++) {
				inputLayer [j] = new Neuron (0, j, false);
			}
			layers.Add (inputLayer);
		}

		private void BuildHiddenLayers (List<Int16> hiddenLayerNeurons)
		{
			for (int i = 0; i < hiddenLayerNeurons.Count; i++) {
				Neuron[] layer = new Neuron[hiddenLayerNeurons [i]];

				for (int j = 0; j < layer.Length; j++) {
					layer [j] = new Neuron (i + 1, j, false);
				}
				layers.Add (layer);
			}
		}

		private void BuildOutputLayer ()
		{
			outputLayer = new Neuron[nOutputs];

			for (int j = 0; j < outputLayer.Length; j++) {
				outputLayer [j] = new Neuron (0, j, true);
			}


			outputLayer [0] = new Neuron (layers.Count, 0, true);

			layers.Add (outputLayer);
		}

		private void MakeConnections ()
		{
			for (int i = 1; i < layers.Count; i++) {
				Neuron[] layer = layers [i];
				for (int j = 0; j < layer.Length; j++) {
					layer [j].InNeurons = layers [i - 1];
				}
			}

			for (int i = 0; i < layers.Count - 1; i++) {
				Neuron[] layer = layers [i];
				for (int j = 0; j < layer.Length; j++) {
					layer [j].OutNeurons = layers [i + 1];
				}
			}

			for (int i = 1; i < layers.Count; i++) {
				Neuron[] layer = layers [i];
				for (int j = 0; j < layer.Length; j++) {
					layer [j].InitWeights ();
				}
			}
		}

		private void LearnNetwork ()
		{
			iter = 0;

			Double learningRmse = Double.MaxValue;
			Double validatingRmse = Double.MaxValue;

			Double oldLearningRmse;
			Double oldValidatingRmse;

			do {
				oldLearningRmse = learningRmse;
				oldValidatingRmse = validatingRmse;

				//Console.WriteLine ("iter: {0}", iter);
				learningRmse = 0.0;
				for (int k = 0; k < noLearning; k++) {
					/* Set output for neurons from input layer. */
					for (int j = 0; j < inputLayer.Length; j++) {
						inputLayer [j].Output = dataSet [k].InValues [j];
					}

					/* Set desired output for neurons from output layer. */
					for (int j = 0; j < outputLayer.Length; j++) {
						outputLayer [j].DesiredOutput = dataSet [k].OutValues [j];
					}

					/* Forward */
					Forward ();
					/* Compute gradient. */
					Gradient ();
					/* Make backpropagation. */
					Back ();

					learningRmse += RootMeanSquareError ();
				}

				learningRmse /= 2;

				ComputeRmse (noLearning, noLearning + noValidating, ref validatingRmse);

				iter++;
			} while (!((oldLearningRmse > learningRmse) && (oldValidatingRmse <= validatingRmse)));
		}

		private Double RootMeanSquareError ()
		{
			return Math.Pow ((outputLayer [0].DesiredOutput - outputLayer [0].Output), 2);
		}

		private Double AbsoluteError ()
		{
			return Math.Abs (outputLayer [0].Output - outputLayer [0].DesiredOutput);
		}

		private Double RelativeError ()
		{
			if (outputLayer [0].DesiredOutput != 0) {
				return Math.Abs (outputLayer [0].Output - outputLayer [0].DesiredOutput) / outputLayer [0].DesiredOutput;
			} else {
				return 0;
			}
		}

		private void Forward ()
		{
			for (int i = 1; i < layers.Count; i++) {
				Neuron[] layer = layers [i];

				for (int j = 0; j < layer.Length; j++) {
					layer [j].Forward ();
				}
			}
		}

		private void Gradient ()
		{
			for (int i = layers.Count - 1; i >= 1; i--) {
				Neuron[] layer = layers [i];

				for (int j = 0; j < layer.Length; j++) {
					layer [j].Gradient ();
				}
			}
		}

		private void Back ()
		{
			for (int i = layers.Count - 1; i >= 1; i--) {
				Neuron[] layer = layers [i];

				for (int j = 0; j < layer.Length; j++) {
					layer [j].Back ();
				}
			}
		}

		private void RunValidatingSet ()
		{

		}

		private void ComputeMeanErrors (Int32 start, Int32 stop, ref Double mae, ref Double mre)
		{
			mae = 0.0;
			mre = 0.0;

			for (int k = start; k < stop; k++) {
				/* Set output for neurons from input layer. */
				for (int j = 0; j < inputLayer.Length; j++) {
					inputLayer [j].Output = dataSet [k].InValues [j];
				}

				/* Set desired output for neurons from output layer. */
				for (int j = 0; j < outputLayer.Length; j++) {
					outputLayer [j].DesiredOutput = dataSet [k].OutValues [j];
				}

				/* Forward */
				Forward ();
				mae += AbsoluteError ();
				mre += RelativeError ();
			}

			mae /= stop - start;
			mre /= stop - start;
		}

		private void ComputeRmse (Int32 start, Int32 stop, ref Double rmse)
		{
			rmse = 0.0;
			for (int k = start; k < stop; k++) {
				/* Set output for neurons from input layer. */
				for (int j = 0; j < inputLayer.Length; j++) {
					inputLayer [j].Output = dataSet [k].InValues [j];
				}

				/* Set desired output for neurons from output layer. */
				for (int j = 0; j < outputLayer.Length; j++) {
					outputLayer [j].DesiredOutput = dataSet [k].OutValues [j];
				}

				/* Forward */
				Forward ();
				rmse += RootMeanSquareError ();
			}

			rmse /= 2;
		}
	}
}

