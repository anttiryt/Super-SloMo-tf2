import tensorflow as tf

from models.layers import BackWarp


def reconstruction_loss(y_true, y_pred):
    return l1_loss(y_true, y_pred)


def l1_loss(y_true, y_pred):
    return tf.reduce_mean(tf.reduce_sum(tf.abs(y_pred - y_true)))


def warping_loss(warping_input):
    # warping_input[0] = frame_0
    # warping_input[1] = frame_1
    # warping_input[2] = frame_t
    return (
        l1_loss(warping_input[0], warping_input[3])
        + l1_loss(warping_input[1], warping_input[4])
        + l1_loss(warping_input[2], warping_input[5])
        + l1_loss(warping_input[2], warping_input[6])
    )


def smoothness_loss(f_01, f_10):
    delta_f_01 = _compute_delta(f_01)
    delta_f_10 = _compute_delta(f_10)
    return 0.5 * (delta_f_01 + delta_f_10)


def _compute_delta(frame):
    return tf.reduce_mean(
        tf.abs(frame[:, 1:, :, :] - frame[:, :-1, :, :])
    ) + tf.reduce_mean(tf.abs(frame[:, :, 1:, :] - frame[:, :, :-1, :]))
