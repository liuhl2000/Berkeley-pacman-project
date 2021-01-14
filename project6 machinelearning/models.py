import nn

class PerceptronModel(object):
    def __init__(self, dimensions):
        self.w = nn.Parameter(1, dimensions)

    def get_weights(self):
        return self.w

    def run(self, x):
        return nn.DotProduct(self.w, x)

    def get_prediction(self, x):
        output_num = nn.as_scalar(self.run(x))
        if output_num >= 0:
            return 1
        else:
            return -1

    def train(self, dataset):
        batch_size = 1
        while True:
            indicator = 0
            for x,y in dataset.iterate_once(batch_size):
                standard_output = nn.as_scalar(y)
                predict_output = self.get_prediction(x)
                if standard_output != predict_output:
                    indicator = 1
                    nn.Parameter.update(self.w, x, standard_output)

            if indicator == 0:
                break


class RegressionModel(object):
    def __init__(self):
        self.W1 = nn.Parameter(1, 50)
        self.b1 = nn.Parameter(1,50)
        self.W2 = nn.Parameter(50,1)
        self.b2 = nn.Parameter(1,1)

        self.layer_num = 2
        self.batch_size = 10
        self.multiplier = -0.01
        self.hidden_layer_size = 50



    def run(self, x):
        first_layer_output = nn.AddBias(nn.Linear(x, self.W1), self.b1)
        hidden_layer_output = nn.ReLU(first_layer_output)
        output = nn.AddBias(nn.Linear(hidden_layer_output, self.W2), self.b2)   
        return output


    def get_loss(self, x, y):
        return nn.SquareLoss(self.run(x), y)


    def train(self, dataset):
        parameter = [self.W1, self.b1, self.W2, self.b2]
        #while nn.as_scalar(self.get_loss(nn.Constant(dataset.x), nn.Constant(dataset.y))) >= 0.02:
        for x,y in dataset.iterate_forever(self.batch_size):
            gradient = nn.gradients(self.get_loss(x,y), parameter)
            for i in range(4):
                parameter[i].update(gradient[i], self.multiplier)
            if nn.as_scalar(self.get_loss(nn.Constant(dataset.x), nn.Constant(dataset.y))) < 0.02:
                break


class DigitClassificationModel(object):
    def __init__(self):
        self.W1 = nn.Parameter(784, 150)
        self.b1 = nn.Parameter(1,150)
        #self.W2 = nn.Parameter(250,250)
        #self.b2 = nn.Parameter(1,250)
        #self.W3 = nn.Parameter(250,10)
        #self.b3 = nn.Parameter(1,10)
        self.W2 = nn.Parameter(150,10)
        self.b2 = nn.Parameter(1,10)

        self.layer_num = 3
        self.batch_size = 100
        self.multiplier = -0.35



    def run(self, x):
        first_layer_output = nn.AddBias(nn.Linear(x, self.W1), self.b1)
        hidden_layer_1_output = nn.ReLU(first_layer_output)
        output_of_second_layer = nn.AddBias(nn.Linear(hidden_layer_1_output, self.W2), self.b2)   
        #hidden_layer_2_output = nn.ReLU(output_of_second_layer)
        #output = nn.AddBias(nn.Linear(hidden_layer_2_output, self.W3), self.b3)  
        return output_of_second_layer

    def get_loss(self, x, y):
        return nn.SoftmaxLoss(self.run(x),y)


    def train(self, dataset):
        #parameter = [self.W1, self.b1, self.W2, self.b2, self.W3, self.b3]
        parameter = [self.W1, self.b1, self.W2, self.b2]
        #while dataset.get_validation_accuracy() < 0.975:
        for x,y in dataset.iterate_forever(self.batch_size):
            gradient = nn.gradients(self.get_loss(x,y), parameter)
            for i in range(4):
                parameter[i].update(gradient[i], self.multiplier)
            if dataset.get_validation_accuracy() >= 0.975:
                break


class LanguageIDModel(object):
    def __init__(self):

        self.num_chars = 47
        self.languages = ["English", "Spanish", "Finnish", "Dutch", "Polish"]

        
        self.W = nn.Parameter(47, 200)
        self.W_hidden = nn.Parameter(200, 200)
        self.b = nn.Parameter(1, 200)

        self.W_last = nn.Parameter(200, 5)
        self.b_last = nn.Parameter(1, 5)

        self.multiplier = -0.15
        self.batch_size = 100


    def run(self, xs):
        current_output = nn.AddBias(nn.Linear(xs[0], self.W), self.b)
        current_output = nn.ReLU(current_output)

        for i in range(1, len(xs)):
        	current_output = nn.AddBias(nn.Add(nn.Linear(xs[i], self.W), nn.Linear(current_output, self.W_hidden)), self.b)
        	current_output = nn.ReLU(current_output)

        output = nn.AddBias(nn.Linear(current_output, self.W_last), self.b_last)
        return output


    def get_loss(self, xs, y):
        return nn.SoftmaxLoss(self.run(xs), y)


    def train(self, dataset):
        parameter = [self.W, self.W_hidden, self.b, self.W_last, self.b_last]
        for x,y in dataset.iterate_forever(self.batch_size):
            gradient = nn.gradients(self.get_loss(x,y), parameter)
            for i in range(5):
                parameter[i].update(gradient[i], self.multiplier)
            if dataset.get_validation_accuracy() >= 0.85:
                break
        
