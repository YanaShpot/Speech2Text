from keras import backend as K
from keras.models import Model
from keras.layers import (BatchNormalization, Conv1D, Dense, Input,
                          TimeDistributed, Activation, Bidirectional, SimpleRNN, GRU, LSTM, Dropout, MaxPooling1D)


def simple_rnn_model(input_dim, output_dim=29):
    input_data = Input(name='the_input', shape=(None, input_dim))
    # Add recurrent layer
    simp_rnn = GRU(output_dim, return_sequences=True,
                   implementation=2, name='rnn')(input_data)
    # Add softmax activation layer
    y_pred = Activation('softmax', name='softmax')(simp_rnn)
    # Specify the model
    model = Model(inputs=input_data, outputs=y_pred)
    model.output_length = lambda x: x
    print(model.summary())
    return model


def rnn_model(input_dim, units, activation, output_dim=29):
    # Main acoustic input
    input_data = Input(name='the_input', shape=(None, input_dim))
    # Add recurrent layer
    simp_rnn = GRU(units, activation=activation,
                   return_sequences=True, implementation=2, name='rnn')(input_data)
    # Add batch normalization
    bn_rnn = BatchNormalization()(simp_rnn)
    # Add a TimeDistributed(Dense(output_dim)) layer
    time_dense = TimeDistributed(Dense(output_dim))(bn_rnn)
    # Add softmax activation layer
    y_pred = Activation('softmax', name='softmax')(time_dense)
    # Specify the model
    model = Model(inputs=input_data, outputs=y_pred)
    model.output_length = lambda x: x
    print(model.summary())
    return model


def cnn_rnn_model(input_dim, filters, kernel_size, conv_stride,
                  conv_border_mode, units, output_dim=29):
    # Main acoustic input
    input_data = Input(name='the_input', shape=(None, input_dim))
    # Add convolutional layer
    conv_1d = Conv1D(filters, kernel_size,
                     strides=conv_stride,
                     padding=conv_border_mode,
                     activation='relu',
                     name='conv1d')(input_data)
    # Add batch normalization
    bn_cnn = BatchNormalization(name='bn_conv_1d')(conv_1d)
    # Add a recurrent layer
    simp_rnn = SimpleRNN(units, activation='relu',
                         return_sequences=True, implementation=2, name='rnn')(bn_cnn)
    # Add batch normalization
    bn_rnn = BatchNormalization()(simp_rnn)
    # Add a TimeDistributed(Dense(output_dim)) layer
    time_dense = TimeDistributed(Dense(output_dim))(bn_rnn)
    # Add softmax activation layer
    y_pred = Activation('softmax', name='softmax')(time_dense)
    # Specify the model
    model = Model(inputs=input_data, outputs=y_pred)
    model.output_length = lambda x: cnn_output_length(
        x, kernel_size, conv_border_mode, conv_stride)
    print(model.summary())
    return model


def cnn_rnn_model_with_dropout(input_dim, filters, kernel_size, conv_stride,
                               conv_border_mode, units, output_dim=29):
    # Main acoustic input
    input_data = Input(name='the_input', shape=(None, input_dim))
    # Add convolutional layer
    conv_1d = Conv1D(filters, kernel_size,
                     strides=conv_stride,
                     padding=conv_border_mode,
                     activation='relu',
                     name='conv1d')(input_data)
    # Add batch normalization
    bn_cnn = BatchNormalization(name='bn_conv_1d')(conv_1d)
    # dropout_layer = Dropout(0.3)(bn_cnn)
    # Add a recurrent layer
    simp_rnn = SimpleRNN(units, activation='relu',
                         return_sequences=True, implementation=2, name='rnn', dropout=0.3, recurrent_dropout=0.3)(
        bn_cnn)
    # Add batch normalization
    bn_rnn = BatchNormalization()(simp_rnn)
    # Add a TimeDistributed(Dense(output_dim)) layer
    time_dense = TimeDistributed(Dense(output_dim))(bn_rnn)
    # Add softmax activation layer
    y_pred = Activation('softmax', name='softmax')(time_dense)
    # Specify the model
    model = Model(inputs=input_data, outputs=y_pred)
    # Pad
    model.output_length = lambda x: cnn_output_length(x,
                                                      kernel_size,
                                                      conv_border_mode,
                                                      conv_stride)
    # Summarize
    print(model.summary())
    return model


def cnn_output_length(input_length, filter_size, border_mode, stride,
                      dilation=1):
    if input_length is None:
        return None
    assert border_mode in {'same', 'valid'}
    dilated_filter_size = filter_size + (filter_size - 1) * (dilation - 1)
    if border_mode == 'same':
        output_length = input_length
    elif border_mode == 'valid':
        output_length = input_length - dilated_filter_size + 1
    return (output_length + stride - 1) // stride


def deep_rnn_model(input_dim, units, recur_layers, output_dim=29):
    # Main acoustic input
    input_data = Input(name='the_input', shape=(None, input_dim))
    # Add recurrent layers, each with batch normalization
    rnn_layer = input_data
    for i in range(recur_layers):
        simp_rnn = GRU(units, activation='relu',
                       return_sequences=True, implementation=2, name='rnn_{}'.format(i + 1))(rnn_layer)
        # Add batch normalization
        bn_rnn = BatchNormalization()(simp_rnn)
        rnn_layer = bn_rnn
    # Add a TimeDistributed(Dense(output_dim)) layer
    time_dense = TimeDistributed(Dense(output_dim))(rnn_layer)
    # Add softmax activation layer
    y_pred = Activation('softmax', name='softmax')(time_dense)
    # Specify the model
    model = Model(inputs=input_data, outputs=y_pred)
    # Pad
    model.output_length = lambda x: x
    # Summarize
    print(model.summary())
    return model


def bidirectional_rnn_model(input_dim, units, output_dim=29):
    # Main acoustic input
    input_data = Input(name='the_input', shape=(None, input_dim))
    # Add bidirectional recurrent layer
    bidir_rnn = Bidirectional(GRU(units, activation='relu', return_sequences=True, implementation=2, name='rnn'))(
        input_data)
    bn_rnn = BatchNormalization()(bidir_rnn)
    # Add a TimeDistributed(Dense(output_dim)) layer
    time_dense = TimeDistributed(Dense(output_dim))(bn_rnn)
    # Add softmax activation layer
    y_pred = Activation('softmax', name='softmax')(time_dense)
    # Specify the model
    model = Model(inputs=input_data, outputs=y_pred)
    # Pad
    model.output_length = lambda x: x
    # Summarize
    print(model.summary())
    return model

def deep_bidirectional_rnn_model(input_dim, units, recur_layers=1, RNN_type=LSTM, output_dim=29):
        # Main acoustic input
        input_data = Input(name='the_input', shape=(None, input_dim))
        # Add recurrent layers, each with batch normalization
        rnn_layer = input_data
        for i in range(recur_layers):
            simp_rnn = Bidirectional(RNN_type(units, activation='relu',
                return_sequences=True, implementation=2, name='bidir_rnn_{}'.format(i + 1)))(rnn_layer)
            # Add batch normalization
            bn_rnn = BatchNormalization()(simp_rnn)
            rnn_layer = bn_rnn
        # Add a TimeDistributed(Dense(output_dim)) layer
        time_dense = TimeDistributed(Dense(output_dim))(rnn_layer)
        # Add softmax activation layer
        y_pred = Activation('softmax', name='softmax')(time_dense)
        # Specify the model
        model = Model(inputs=input_data, outputs=y_pred)
        # Pad
        model.output_length = lambda x: x
        # Summarize
        print(model.summary())
        return model

def final_model_upd(input_dim, filters, kernel_size, conv_stride,conv_border_mode, units, recur_layers=3, RNN_type=GRU, dropout=0.2, output_dim=29):
    # TODO: Сheck dropout
    # TODO: Consider maxpooling
    # Main acoustic input
    input_data = Input(name='the_input', shape=(None, input_dim))
    # Add convolutional layer
    conv_1d = Conv1D(filters, kernel_size, 
                     strides=conv_stride, 
                     padding=conv_border_mode,
                     activation='relu',
                     name='conv1d')(input_data)
    # Add batch normalization
    bn_cnn = BatchNormalization(name='bn_conv_1d')(conv_1d)
    rnn_layer = bn_cnn
    for i in range(recur_layers):
        simp_rnn = Bidirectional(RNN_type(units, activation='relu',
                                          return_sequences=True, implementation=2, recurrent_dropout=dropout, dropout=dropout, name='bidir_rnn_{}'.format(i + 1)))(rnn_layer)
        # Add batch normalization
        bn_rnn = BatchNormalization()(simp_rnn)
        rnn_layer = bn_rnn
    time_dense = TimeDistributed(Dense(output_dim))(rnn_layer)
    y_pred = Activation('softmax', name='softmax')(time_dense)
    # Specify the model
    model = Model(inputs=input_data, outputs=y_pred)
    # TODO: Specify model.output_length
    model.output_length = lambda x: cnn_output_length(x, kernel_size, conv_border_mode, conv_stride)
    print(model.summary())
    return model