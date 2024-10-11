import warnings
from math import sqrt

from misc.disambiguate import disambiguate
from parse.quickparse import quickparse
from sample.sample import sample
from volume.slice_volume import slice_volume
from os.path import join
from scipy.stats import norm, beta


def volume_estimate(node, n, nr_samples, gamma = 0.95, T = None, mode ='wald'):
    """
    Gives an estimated volume and a confidence interval for the given expression.
    :param node: expression (should be ambiguous)
    :param n: fixed length of words.
    :param gamma: confidence niveau. gamma = 1-alpha, gamme
    :param T: Optional fixed duration. If duration is not set, we do the procedure for total volume.
    This fails in case of unbounded expressions.
    :return: volume estimate, confidence interval
    """

    alpha = 1 - gamma

    print(f"$\\varphi = {node.getText()}$")
    print(f"$\\varphi = {disambiguate(node)}$")

    V = slice_volume(quickparse(disambiguate(node), string=True), n)
    # V.fancy_print()
    # V.plot()

    counts = []

    with warnings.catch_warnings():
        warnings.filterwarnings("error", category=UserWarning)

        for i in range(nr_samples):
            w, feedback = sample(node, n, feedback=True)
            counts.append(feedback.smart_rej)  # the rejections of the smart rej sampling

    k = nr_samples
    N = sum(counts) + k

    match mode:
        case 'wald':

            # Wald confidence interval:
            # https://de.wikipedia.org/wiki/Konfidenzintervall_f%C3%BCr_die_Erfolgswahrscheinlichkeit_der_Binomialverteilung
            p_hat = k / N

            c = norm.ppf(1 - (1-gamma)/2)
            print('test:',norm.cdf(c))
            st_err = sqrt(p_hat * (1 - p_hat) / N)
            p_a, p_b = p_hat - c * st_err, p_hat + c * st_err

            v_est = V.total_volume() * p_hat
            a_vol, b_vol = V.total_volume() * p_a, V.total_volume() * p_b

        case 'pearson':
            p_hat = k / N
            p_a = beta.ppf(1- (1-alpha/2),k,N - k + 1)
            p_b = beta.ppf(1-alpha/2,k+1,N - k)

            v_est = p_hat * V.total_volume()
            a_vol, b_vol = p_a * V.total_volume(), p_b * V.total_volume()

        case _:
            raise NotImplementedError

    print(f"Confidence interval of p (mode={mode}):[{p_a},{p_b}]")
    print(f"V(e') =       \t{V.total_volume()}")
    print(f"Accepted...   \t{nr_samples}")
    print(f"Rejections... \t{sum(counts)}")
    if sum(counts) == 0:
        warnings.warn(f"No rejections for {nr_samples} samples. This most likely means that the expression was "
                      f"unambiguous and the confidence interval might be nonsense. \n "
                      f"If it is unambiguous, the volume will be:\n{slice_volume(node, n)}.")

    print(f"Volume estimate for {node.getText()}. n={n} is {v_est}.")
    print(f"Or rather: With confidence {gamma} the estimated volume is in [{a_vol}, {b_vol}] ({mode} CI).")

    return v_est, (a_vol, b_vol)


if __name__ == '__main__':
    ctx = quickparse(join('experiments', 'spec_09_ambig.tre'))
    n = 1
    # T = 1.7
    nr_samples = 1000
    conf = 0.95

    v_est, (a,b) = volume_estimate(node=ctx, n=n, nr_samples=nr_samples, gamma=conf, mode='pearson')