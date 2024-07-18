# Dynamic Serverless Pricing (DSP) Model

Serverless computing has recently become very popular because it simplifies deploying and scaling applications. It lets users develop and run code in the form of Function-as-a-Service (FaaS) without worrying about the underlying infrastructures. It promises pay-as-you-go pricing based on usage.

However, current pricing models in serverless computing are often static, charging based on execution time and memory usage. The static pricing model can be inefficient, as it needs to account for changes in demand and usage over time, leading to higher costs for developers. This static pricing model fails to reflect the real-time fluctuations in resource demand and availability, resulting in suboptimal pricing that does not always align with the actual value or cost of the resources consumed. Furthermore, it does not incentivize efficient resource utilization (i.e., cheaper resources in inactive times) or offer competitive pricing that could benefit both providers and users.

In this paper, we introduce a Dynamic Serverless Pricing (DSP) model that uses game theory to manage costs and resources better. The DSP model utilizes the Stackelberg game to adjust prices based on demand and usage patterns, encouraging server providers to take advantage of off-peak hours. We evaluated the effectiveness of our approach and the experimental results showed that our proposed pricing model reduces the cost by up to 25% and increases resource utilization compared with the existing pricing model.

## Repository Structure

- **src/**: Contains the source code for the DSP model.
- **data/**: Includes datasets used for the experiments.
- **results/**: Contains the results of our experiments and evaluations.
- **README.md**: Overview of the project and instructions.


## License

This project is licensed under the MIT License .

## Contact

For any questions or suggestions, please contact [javadghasemiro@gmail.com](mailto:javadghasemiro@gmail.com).
